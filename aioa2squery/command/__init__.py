import asyncio
import logging

from .arguments import cmd_args
from .proxy import *
from .query import *
from .server import *

__all__ = (
    'main',
)


def main():
    try:
        import uvloop
        logging.debug("Setting default event loop implementation to uvloop")
        uvloop.install()
    except ImportError as err:
        logging.debug("Unable to import uvloop: %s", err)

    loop = asyncio.get_event_loop()

    if logging.root.level is logging.DEBUG:
        loop.set_debug(True)

    try:
        if cmd_args.command == 'query':
            query(loop)
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
