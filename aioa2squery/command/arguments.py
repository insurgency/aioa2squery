import argparse
import logging
import re
from argparse import Action, _ArgumentGroup

from typing import Iterable, Text, List, Optional

from ipaddress import ip_network

from .. import QueryPort


def port_range_expression(port_range_expr: str) -> Iterable[int]:
    port_list = set()

    try:
        for port in set(port_range_expr.split(',')):
            if '-' in port:
                start_port, end_port = port.split('-', 1)
                start_port, end_port = int(start_port), int(end_port)
                assert 0 <= start_port < end_port <= 2 ** 16 - 1

                port_list.update(range(start_port, end_port + 1))
            else:
                port = int(port)
                assert 0 <= port <= 2 ** 16 - 1

                port_list.add(port)
    except (ValueError, AssertionError):
        raise argparse.ArgumentTypeError
    else:
        return port_list


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Titleize positional and optional argument group titles
        self._positionals.title = self._positionals.title.title()
        self._optionals.title = self._optionals.title.title()

    def convert_arg_line_to_args(self, arg_line: Text) -> List[str]:
        # Remove any text that's commented out
        # language=PythonRegExp
        arg_line = re.sub(pattern=r'#.*\n?', repl='', string=arg_line)
        # Strip leading & trailing whitespace from each line
        arg_line = arg_line.strip()

        return arg_line.split()


# noinspection PyProtectedMember
class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '

        super().add_usage(usage, actions, groups, prefix)

    def _format_action(self, action: argparse.Action):
        parts = super()._format_action(action)

        if action.nargs == argparse.PARSER:
            parts = '\n'.join(parts.split('\n')[1:])

        return parts


# Main argument parser
parser = ArgumentParser(prog='a2squery', fromfile_prefix_chars='@', formatter_class=HelpFormatter,
                        description="Command-line utility for the A2S game server query protocol")
# Monkey patch fromfile_prefix_chars parsing with fancier reading capabilities for main parser
# parser.convert_arg_line_to_args = convert_arg_line_to_args
# Title-ize parser's positional and optional arguments title text

# Main parser arguments
parser.add_argument('-v', '--version', action='version', version='%(prog)s')  # FIXME
# noinspection PyProtectedMember
parser.add_argument('-l', '--log-level', type=str.upper, help=argparse.SUPPRESS, choices=logging._nameToLevel.keys())

# Create a action object for main argument parser
subparsers = parser.add_subparsers(title='Commands', dest='command', required=True, metavar='<command>')

# Query sub-command/subparser
_ = "Query game servers"
query_subparser = subparsers.add_parser('query', help=_, description=_, formatter_class=HelpFormatter)

# Query type argument group
query_type_arg_group = query_subparser.add_argument_group(title="Query Type",
                                                          description="Type of server query to perform")
query_type_group = query_type_arg_group.add_mutually_exclusive_group(required=True)
query_type_group.add_argument('--info', action='store_true', help="Query server information")
query_type_group.add_argument('--players', action='store_true', help="Query servers' online players")
query_type_group.add_argument('--rules', action='store_true', help="Query server rules")
query_type_group.add_argument('--ping', action='store_true', help="Query server ping")

# Query subparser arguments
query_subparser.add_argument('-p', '--ports', help="Destination ports", metavar='PORTS', type=port_range_expression,
                             default={int(QueryPort.SRCDS)})
query_subparser.add_argument('-t', '--timeout', default=3, type=float, help="Query timeout duration", metavar='SECONDS')
query_subparser.add_argument('networks', nargs='+', metavar='CIDR', help="Network to query", type=ip_network)
# Some additional super "secret" developer query options
query_subparser.add_argument('--csv', action='store_true', default=False, help=argparse.SUPPRESS)
query_subparser.add_argument('-c', '--concurrency', default=50, type=int, help=argparse.SUPPRESS)

# Query app argument group
query_app_group = query_subparser.add_argument_group(title='App & Engine Type',
                                                     description="App ID or game engine version to query")
query_app_group.add_argument('--app', dest='app_id', default=None, type=int, help="Query specific App ID", metavar='ID')
query_app_group.add_argument('--source', '--source-engine', action='store_true',
                             help="Perform Source Engine queries (default)")
query_app_group.add_argument('--goldsrc', '--goldsource', action='store_true', help="Perform GoldSrc queries")

# Listen sub-command/subparser
_ = "Run a static query server"
listen_subparser = subparsers.add_parser('listen', description=_, help=_, formatter_class=HelpFormatter)

# Proxy sub-command/subparser
_ = "Run a reverse proxy server"
proxy_subparser = subparsers.add_parser('proxy', description=_, help=_, formatter_class=HelpFormatter)

# Finally parse arguments
cmd_args = parser.parse_args()
