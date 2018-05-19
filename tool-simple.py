#!/usr/bin/env python

#
# Minimal command line tool skeleton
#
# Maintained at https://github.com/liyanage/python-modules
#

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys
import os
import re
import argparse
import logging


class Tool(object):

    def __init__(self, args):
        self.args = args

    def run(self):
        print(self.args.path)

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser(description='Description')
        parser.add_argument('path', help='Path to something')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose debug logging')

        args = parser.parse_args()
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)

        cls(args).run()


if __name__ == "__main__":
    Tool.main()
