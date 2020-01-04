import argparse
import ipaddress
import itertools
import logging
import re
import sys

from typing import Iterable, Text, List, Union, Sequence, Any, Optional

from argparse import Namespace

from .. import QueryPort

# Localization/GNU gettext
try:
    from gettext import gettext as _, ngettext
except ImportError:
    def _(message):
        return message


    def ngettext(singular, plural, n):
        if n == 1:
            return singular
        else:
            return plural


def port_range_expression(port_range_expr: str) -> Iterable[int]:
    port_list = set()

    try:
        for port in set(port_range_expr.split(',')):
            if '-' in port:
                start_port, end_port = port.split('-', 1)
                start_port, end_port = int(start_port), int(end_port)
                if not 0 <= start_port < end_port <= 2 ** 16 - 1:
                    raise ValueError

                port_list.update(range(start_port, end_port + 1))
            else:
                port = int(port)
                if not 0 <= port <= 2 ** 16 - 1:
                    raise ValueError

                port_list.add(port)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid port expression {port_range_expr}")

    return port_list


def ip_network(address: str):
    try:
        if '-' in address:
            # Process network range notation in a special way:
            address_range = map(ipaddress.IPv4Address, address.split('-', maxsplit=1))

            return list(ipaddress.summarize_address_range(*address_range))
        else:
            # Otherwise apply normal CIDR notation parsing
            return [ipaddress.IPv4Network(address)]
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"invalid IPv4 network value '{address}'")


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Capitalize the default help action help text
        self._actions[0].help = self._actions[0].help.capitalize()

        # Titleize positional and optional argument group titles
        self._positionals.title = self._positionals.title.title()
        self._optionals.title = self._optionals.title.title()

    def convert_arg_line_to_args(self, arg_line: Text) -> List[str]:
        # Remove any text that's commented out
        # language=PythonRegExp
        arg_line = re.sub(pattern=r'#.*\n?', repl='', string=arg_line)
        # Strip leading & trailing whitespace from each line
        arg_line = arg_line.strip()
        # Split line at whitespace seperations
        arg_line = arg_line.split()

        return arg_line

    def error(self, message: Text):
        self.print_usage(sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self.exit(2, _('Error: %(message)s\n') % args)


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = _('Usage: ')

        super().add_usage(usage, actions, groups, prefix)

    # noinspection PyProtectedMember
    def _format_action(self, action: argparse.Action):
        parts = super()._format_action(action)

        if action.nargs == argparse.PARSER:
            parts = '\n'.join(parts.split('\n')[1:])

        return parts


class ChainAndCollapseIPNetworksAction(argparse.Action):
    def __call__(self, arg_parser: ArgumentParser, namespace: Namespace, networks: Union[Text, Sequence[Any], None],
                 option_string: Optional[Text] = ...):
        # Flatten iterable of iterable of IPv4 network objects
        networks = itertools.chain.from_iterable(networks)
        # Collapse overlapping IPv4 networks in order avoid querying duplicate IP addresses
        networks = list(ipaddress.collapse_addresses(networks))
        setattr(namespace, self.dest, networks)


# Main argument parser
parser = ArgumentParser(prog='a2squery', fromfile_prefix_chars='@', formatter_class=HelpFormatter,
                        description="Command-line utility for the A2S game server query protocol")

# Main parser arguments
# FIXME
# noinspection PyProtectedMember
parser.add_argument('-v', '--version', action='version', version='%(prog)s',
                    # Capitalize default version argument help text
                    help=argparse._VersionAction.__init__.__defaults__[-1].capitalize())
# noinspection PyProtectedMember
parser.add_argument('-l', '--log-level', type=str.upper, help=argparse.SUPPRESS, choices=logging._nameToLevel.keys())

# Create a action object for main argument parser
subparsers = parser.add_subparsers(title='Commands', dest='command', required=True, metavar='<command>')

# Query sub-command/subparser
_help = "Query game servers"
query_subparser = subparsers.add_parser('query', help=_help, description=_help, formatter_class=HelpFormatter)

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
query_subparser.add_argument('-i', '--input-file', type=argparse.FileType('r'),
                             help="Query networks from an external FILE", metavar='FILE')
query_subparser.add_argument('networks', action=ChainAndCollapseIPNetworksAction, nargs='*', metavar='CIDR',
                             help="Network to query", type=ip_network)
# Some additional super "secret" developer query options
query_subparser.add_argument('--csv', action='store_true', default=False, help=argparse.SUPPRESS)
query_subparser.add_argument('-c', '--concurrency', default=250, type=int, help=argparse.SUPPRESS)

# Query app argument group
query_app_group = query_subparser.add_argument_group(title='App & Engine Type',
                                                     description="App ID or game engine version to query")
query_app_group.add_argument('--app', dest='app_id', default=None, type=int, help="Query specific App ID", metavar='ID')
query_engine_group = query_app_group.add_mutually_exclusive_group()
query_engine_group.add_argument('--source', '--source-engine', action='store_true',
                                help="Perform Source Engine queries (default)")
query_engine_group.add_argument('--goldsrc', '--goldsource', action='store_true', help="Perform GoldSrc queries")

# Listen sub-command/subparser
_help = "Run a static query server"
listen_subparser = subparsers.add_parser('listen', description=_help, help=_help, formatter_class=HelpFormatter)

# Proxy sub-command/subparser
_help = "Run a reverse proxy server"
proxy_subparser = subparsers.add_parser('proxy', description=_help, help=_help, formatter_class=HelpFormatter)

# Finally parse arguments
cmd_args = parser.parse_args()

if cmd_args.command == 'query':
    # Require at least one target host to be passed as a positional command argument or from a parsed file
    if not (cmd_args.networks or cmd_args.input_file):
        parser.error("At least one network or host to query must be provided")

    if cmd_args.csv and not cmd_args.info:
        parser.error("--csv option can only be applied to --info queries")

    # Parse networks from a file if the file argument was passed
    if cmd_args.input_file:
        for line_number, line_text in enumerate(cmd_args.input_file.read().splitlines(), 1):
            networks_from_line = parser.convert_arg_line_to_args(line_text)

            for network in networks_from_line:
                try:
                    network = ip_network(network)
                except argparse.ArgumentTypeError:
                    parser.error(f"invalid network '{network}' in '{cmd_args.input_file.name}' (line {line_number})")
                else:
                    cmd_args.networks.extend(network)

        # Collapse overlapping networks again after file containing networks is parsed
        cmd_args.networks = list(ipaddress.collapse_addresses(cmd_args.networks))

# Set logging level with a basic config to the configured level
logging.basicConfig(format='%(levelname)s (%(name)s): %(message)s', level=cmd_args.log_level or logging.INFO)
