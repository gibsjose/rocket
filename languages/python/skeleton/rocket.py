#!/usr/bin/env python3

#   {TITLE}
#   {DESCRIPTION}
#
#   {DD MONTH YYYY}
#
#   {AUTHOR-NAME} ({AUTHOR-EMAIL})
#
#   {LICENSE}
#
#   {WEBSITE}

from enum import Enum
import sys
import os
import traceback
import argparse
import re
import operator
import time

def main():
    global args

    if args.verbose:
        print('OPTIONS')
        print('-------')
        print('\tFlag: ' + str(args.flag))

    if args.command == 'print':
        print(args.choice)

    elif args.command == 'hello':
        print('Hey there!')

    else:
        print('Rocket!')

if __name__ == '__main__':
    try:
        start_time = time.time()

        parser = argparse.ArgumentParser(prog='rocket', description='some awesome new Python script')

        # Options
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose mode')
        parser.add_argument('-f', '--flag', action='store_true', default=False, help='useless flag')

        # Commands
        subparsers = parser.add_subparsers(help='commands:', dest='command')

        run_parser = subparsers.add_parser('print', help='print something')
        run_parser.add_argument('choice', type=str.lower, help='stuff to print', choices=['hello', 'goodbye'])

        hello_parser = subparsers.add_parser('hello', help='say helllo')

        args = parser.parse_args()

        main()
        if args.verbose: print('\n' + time.asctime())
        if args.verbose: print('Total Runtime: ', end='')
        if args.verbose: print(str((time.time() - start_time) * 1000) + ' ms')
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        print('Error: Unexpected Exception')
        print(str(e))
        traceback.print_exc()
        os._exit(1)
