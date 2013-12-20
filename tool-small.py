#!/usr/bin/env python

#
# Minimal command line tool skeleton
#
# Maintained at https://github.com/liyanage/python-modules
#

import sys
import os
import re
import argparse
import logging


class AbstractSubcommand(object):

    def __init__(self, arguments):
        self.args = arguments

    def run(self):
        pass

    @classmethod
    def configure_argument_parser(cls, parser):
        pass

    @classmethod
    def subcommand_name(cls):
        return '-'.join([i.lower() for i in re.findall(r'([A-Z][a-z]+)', re.sub(r'^Subcommand', '', cls.__name__))])


class SubcommandExample(AbstractSubcommand):
    """
    Usage/Documentation for this subcommand
    """
    
    def run(self):
        print 'Hello world'


class Tool(object):

    def subcommand_map(self):
        return {subclass.subcommand_name(): subclass for subclass in AbstractSubcommand.__subclasses__()}

    @classmethod
    def main(cls):
        cls().run()

    def run(self):
        parser = argparse.ArgumentParser(description='Description')
        parser.add_argument('--some_global_option', help='Description')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose debug logging')
        subparsers = parser.add_subparsers(title='Subcommands', dest='subcommand_name')

        subcommand_map = self.subcommand_map()
        for subcommand_name, subcommand_class in subcommand_map.items():
            subparser = subparsers.add_parser(subcommand_name, help=subcommand_class.__doc__)
            subcommand_class.configure_argument_parser(subparser)

        args = parser.parse_args()
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)

        subcommand_class = subcommand_map[args.subcommand_name]
        subcommand_class(args).run()


if __name__ == "__main__":
    Tool.main()
