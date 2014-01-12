#!/usr/bin/env python

#
# Fancy command line tool skeleton
#
# If you want a single-file tool, you can either rename and adapt the
# FooTool class at the bottom of this file, or even directly adapt the
# Tool class and eliminate the subclass.
#
# In a larger project, you might want to maintain your tool subclass in
# a separate file and keep this tool_base.py file unchanged so you can
# easily update to never upstream versions. In that case, your subclass
# file would look something like this:
#
#     #!/usr/bin/env python
#
#     from . import tool_base
#     from . import my_module
#
#
#     class MyTool(tool_base.Tool):
#         """My useful tool"""
#
#         pass
#
#
#     class SubcommandDoSomethign(tool_base.AbstractSubcommand):
#         """Descripte the DoSomething subcommand"""
#
#         def run(self):
#             print 'Hello world'
#
#         @classmethod
#         def configure_argument_parser(cls, parser):
#             parser.add_argument('path', help='Path to some useful file')
#             parser.add_argument('-o', '--option', action='store_true', help='Some option')
#
#
#     if __name__ == "__main__":
#         MyTool.main()
#
#
# Maintained at https://github.com/liyanage/python-modules
#

import sys
import os
import re
import argparse
import collections
import contextlib
import logging


class ANSIColor(object):

    red = '1'
    green = '2'
    yellow = '3'
    blue = '4'

    @classmethod
    @contextlib.contextmanager
    def terminal_color(cls, stdout_color=None, stderr_color=red):

        if stdout_color:
            sys.stdout.write(cls.start_sequence(stdout_color))
        if stderr_color:
            sys.stderr.write(cls.start_sequence(stderr_color))

        try:
            yield
        except:
            cls.clear()
            raise

        cls.clear()

    @classmethod
    def clear(cls):
        for stream in [sys.stdout, sys.stderr]:
            stream.write(cls.clear_sequence())

    @classmethod
    def start_sequence(cls, color=red):
        return "\x1b[3{0}m".format(color)

    @classmethod
    def clear_sequence(cls):
        return "\x1b[m"

    @classmethod
    def wrap(cls, value, color=red):
        return u'{}{}{}'.format(cls.start_sequence(color), value, cls.clear_sequence())


class AbstractSubcommand(object):
    """
    A base class for custom subcommand plug-in classes.

    Derive from this class for your custom subcommand extension classes.
    It also documents the interface you are expected to implement in your class
    and it provides some convenience methods.

    :param argparse.Namespace arguments: The command-line options passed to your subcommand
                                         in the form of a namespace instance as returned by
                                         :py:meth:`argparse.ArgumentParser.parse_args`.

    """

    def __init__(self, arguments):
        self.args = arguments

    def run(self):
        """
        This gets called to perform the command's action.

        """
        pass

    @classmethod
    def configure_argument_parser(cls, parser):
        """
        If you override this in your subclass, you can configure additional command line arguments
        for your subcommand's arguments parser.

        :param argparse.ArgumentParser parser: The argument parser that you can configure.

        """
        pass

    @classmethod
    def subcommand_name(cls):
        return '-'.join([i.lower() for i in re.findall(r'([A-Z][a-z]+)', re.sub(r'^Subcommand', '', cls.__name__))])

    @classmethod
    def subclass_map(cls):
        map = {c.__name__: c for c in cls.__subclasses__()}
        for subclass in map.values():
            map.update(subclass.subclass_map())
        return map


class Tool(object):
    """Description for usage message"""

    def subcommand_map(self):
        return {subclass.subcommand_name(): subclass for subclass in AbstractSubcommand.subclass_map().values()}

    def resolve_subcommand_abbreviation(self, subcommand_map):
        non_option_arguments = [i for i in sys.argv[1:] if not i.startswith('-')]
        if not non_option_arguments:
            return True

        subcommand = non_option_arguments[0]
        if subcommand in subcommand_map.keys():
            return True

        # converts a string like 'abc' to a regex like '(a).*?(b).*?(c)'
        regex = re.compile('.*?'.join(['(' + char + ')' for char in subcommand]))
        subcommand_candidates = []
        for subcommand_name in subcommand_map.keys():
            match = regex.match(subcommand_name)
            if not match:
                continue
            subcommand_candidates.append(self.subcommand_candidate_for_abbreviation_match(subcommand_name, match))

        if not subcommand_candidates:
            return True

        if len(subcommand_candidates) == 1:
            print >> sys.stderr, subcommand_candidates[0].decorated_name
            sys.argv[sys.argv.index(subcommand)] = subcommand_candidates[0].name
            return True

        print >> sys.stderr, 'Ambiguous subcommand "{}": {}'.format(subcommand, ', '.join([i.decorated_name for i in subcommand_candidates]))
        return False

    def subcommand_candidate_for_abbreviation_match(self, subcommand_name, match):
        SubcommandCandidate = collections.namedtuple('SubcommandCandidate', ['name', 'decorated_name'])
        decorated_name = ''
        for i in range(1, match.lastindex + 1):
            span = match.span(i)
            preceding = subcommand_name[match.span(i - 1)[1]:span[0]] if span[0] else ''
            letter = subcommand_name[span[0]:span[1]]
            decorated_name += preceding + ANSIColor.wrap(letter, color=ANSIColor.green)
        trailing = subcommand_name[span[1]:]
        decorated_name += trailing
        return SubcommandCandidate(subcommand_name, decorated_name)

    def configure_argument_parser(self, parser):
        pass
        #parser.add_argument('--some_global_option', help='Description')

    def run(self):
        subcommand_map = self.subcommand_map()
        if not self.resolve_subcommand_abbreviation(subcommand_map):
            exit(1)

        parser = argparse.ArgumentParser(description=self.__doc__)
        self.configure_argument_parser(parser)
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose debug logging')
        subparsers = parser.add_subparsers(title='Subcommands', dest='subcommand_name')
        for subcommand_name, subcommand_class in subcommand_map.items():
            subparser = subparsers.add_parser(subcommand_name, help=subcommand_class.__doc__)
            subcommand_class.configure_argument_parser(subparser)

        args = parser.parse_args()
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)

        subcommand_class = subcommand_map[args.subcommand_name]
        subcommand_class(args).run()

    @classmethod
    def main(cls):
        tool = cls()
        tool.run()




class FooTool(Tool):
    """Describe Foo Tool"""

    pass


class SubcommandBar(AbstractSubcommand):
    """List build settings that are defined in a project file, either at the project or target level."""

    def run(self):
        print 'Hello world'

    @classmethod
    def configure_argument_parser(cls, parser):
        parser.add_argument('path', help='Path to some file')
        parser.add_argument('-o', '--option', action='store_true', help='Some option')


if __name__ == "__main__":
    FooTool.main()
