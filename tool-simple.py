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


class Tool(object):

    def __init__(self, args):
        self.args = args

    def run(self):
        print self.args.some_path

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser(description='Description')
        parser.add_argument('some_path', help='Path to something')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose debug logging')

        args = parser.parse_args()
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)

        cls(args).run()


if __name__ == "__main__":
    Tool.main()
