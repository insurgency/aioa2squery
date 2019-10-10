import asyncio
import contextvars
import csv
import logging

from typing import Generator, Tuple, Set

from asyncio import Task, AbstractEventLoop
from dataclasses import fields, asdict
from datetime import timedelta
from ipaddress import IPv4Address
from itertools import chain
from string import printable
from sys import stdout
from textwrap import dedent

from .. import (
    A2SInfoGoldSrcResponse,
    A2SInfoResponse,
    A2SPlayersResponse,
    A2SQueryContext,
    Engine,
    ResponseError,
    A2SRulesResponse,
)
from .arguments import cmd_args

__all__ = (
    'query',
)

successes = errors = players = total_ping = total_players = total_servers = 0
tasks = set()
# Some contextvars for storing information related to our print callback function
remote_addr_var, remote_port_var = contextvars.ContextVar('remote_addr'), contextvars.ContextVar('remote_port')
query_host_var = contextvars.Context()

# Create list of CSV field names by dynamically parsing non-protected members of the A2S_INFO response dataclass
csv_field_names = ['host', 'port', 'ping'] + [f.name for f in fields(A2SInfoResponse) if not f.name.startswith('_')]
# Append any response fields unique to GoldSrc A2S_INFO responses
goldsrc_field_names = [f.name for f in fields(A2SInfoGoldSrcResponse)]
csv_field_names += filter(lambda f: not f.startswith('_') and f not in csv_field_names, goldsrc_field_names)
csv_writer = csv.DictWriter(stdout, fieldnames=csv_field_names)
# Remove some GoldSrc A2S_INFO fields we almost never really care about
csv_field_names.remove('address')


async def query_host(query_client, host, port):
    if cmd_args.info:
        return await query_client.query_info(host, port)
    elif cmd_args.players:
        return await query_client.query_players(host, port)
    elif cmd_args.rules:
        return await query_client.query_rules(host, port)
    elif cmd_args.ping:
        return await query_client.query_ping(host, port)


def print_query_result(ping_task: Task):
    host, port = remote_addr_var.get(), remote_port_var.get()

    try:
        response, ping = ping_task.result()

        if cmd_args.info:
            response: A2SInfoResponse

            global total_players
            total_players += response.players

            if hasattr(response, 'keywords') and response.keywords:
                response.keywords = set(response.keywords.strip(',').split(','))
                response.keywords = ', '.join(sorted(response.keywords))

            if cmd_args.csv:
                # noinspection PyDataclass
                row = {k: v for k, v in asdict(response).items() if not k.startswith('_')}

                # Remove some GoldSrc A2S_INFO fields we almost never really care about
                if 'address' in row:
                    del row['address']
                if 'port' in row:
                    del row['port']

                row = {'host': host, 'port': port, 'ping': ping, **row}
                csv_writer.writerow(row)
            else:
                print(dedent(
                    f"""
                    Host: {host}:{port} ({ping}ms)
                    Name: {response.name}
                    Game: {response.game} ({response.version})
                    App ID: {response.game_id or response.app_id}
                    Visibility: {response.server_visibility}
                    Players: {response.players - response.bots}/{response.max_players} ({response.bots} bots)
                    VAC: {'yes' if response.vac else 'no'}
                    Environment: {response.server_environment!s}
                    Type: {response.server_type!s}
                    Keywords: {response.keywords}
                    """.rstrip()
                ))
        elif cmd_args.players:
            # noinspection PyTypeChecker
            response: A2SPlayersResponse = response

            global players
            players += len(response)

            print(f"Host: {host}:{port} ({len(response)} players)\n")

            # Only print out a table of the players if there is at least one player online
            if response:
                # Print out a fancy table heading
                print(' '.join(('Name'.ljust(32), 'Score', 'Duration')))
                print(' '.join(('-' * 32, '-' * 5, '-' * 8)))

                # Organize the rows of players online by their score descending
                for player in sorted(response.players, key=lambda p: p.score, reverse=True):
                    # Strip characters that don't have a fixed-width from each player's name
                    player.name = ''.join(filter(lambda c: c if c in printable else '?', player.name))
                    player.duration = timedelta(seconds=round(player.duration.total_seconds()))
                    print(f"{player.name.ljust(32)} {str(player.score).ljust(5)} {str(player.duration).ljust(8)}")

                print()
        elif cmd_args.rules:
            response: A2SRulesResponse

            print(f"Host: {host}:{port}\n")
            for name, value in response.rules.items():
                print(f'{name} "{value}"')
        elif cmd_args.ping:
            global total_ping
            total_ping += response

            print(f"{host}:{port}: {response}ms")
    except asyncio.TimeoutError:
        logging.debug(f"{remote_addr_var.get()}:{remote_port_var.get()}: query timed out")
    except ResponseError as err:
        logging.debug(f"{remote_addr_var.get()}:{remote_port_var.get()}: {err}")
    else:
        global successes
        # Increment the total of successfully completed queries for reporting a final summary at the end
        successes += 1
    finally:
        # Always remove the query from task pool and release semaphore counter even if the query didn't succeeded
        tasks.remove(ping_task)
        sem.release()


def hosts(networks, ports: Set[int]) -> Generator[Tuple[IPv4Address, int], None, None]:
    """A more suitable implementation of :class:`itertools.product`"""

    for network in networks:
        for port in ports:
            yield (network, port)


async def query(loop: AbstractEventLoop):
    # Count up the total amount of hosts and target ports being queried
    total_hosts = sum(n.num_addresses for n in cmd_args.networks) * len(cmd_args.ports)
    # Additionally report what the approximate query rate will be given the concurrency and timeout
    query_rate = round(cmd_args.concurrency / cmd_args.timeout)
    # Calculate an **extremely** rough estimate of how long all queries should take to complete
    estimated_time = timedelta(seconds=round(total_hosts / (cmd_args.concurrency / cmd_args.timeout)))

    logging.info(f"Querying {total_hosts:,d} hosts in ~{estimated_time} @ ~{query_rate:,d} queries/sec")

    if cmd_args.info and cmd_args.csv:
        # Print out the CSV header if applicable
        csv_writer.writeheader()

    before = loop.time()

    global sem
    sem = asyncio.BoundedSemaphore(cmd_args.concurrency)

    query_client = A2SQueryContext(timeout=cmd_args.timeout, game_engine=Engine.GOLDSRC if cmd_args.goldsrc else Engine.SOURCE)

    for host, port in hosts(chain.from_iterable(cmd_args.networks), cmd_args.ports):
        await sem.acquire()

        task = asyncio.create_task(query_host(query_client, host=str(host), port=port))
        tasks.add(task)
        remote_addr_var.set(str(host)), remote_port_var.set(port)
        task.add_done_callback(print_query_result)

    await asyncio.gather(*tasks, return_exceptions=True)

    # Calculate some final statistics to report:
    now = loop.time()
    elapsed_time = timedelta(seconds=round(now - before))
    percentage = successes / total_hosts * 100 if total_hosts > 0 else 0

    logging.info(f"Completed {successes:,d}/{total_hosts:,d} ({percentage:.1f}%) queries in {elapsed_time}")

    if successes > 0:
        if cmd_args.info or cmd_args.players:
            logging.info(f"Found a total of {total_players:,d} players online")
        elif cmd_args.ping and successes >= 1:
            logging.info(f"Average server ping of {round(total_ping / successes)}ms")
