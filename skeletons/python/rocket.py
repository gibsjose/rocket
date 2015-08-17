#!/usr/bin/env python3

#   {TITLE}
#
#   {AUTHORS}
#
#   {DD MONTH YYYY}
#
#   {WEBSITES}

from enum import Enum
import sys, os, traceback, optparse
import re
import operator
import time

def main():
    global options, args

    if options.verbose:
        print('OPTIONS')
        print('-------')
        print('\tFlag: ' + str(options.flag))

        if options.file:
            print('\tFile: ' + options.file)

    print('Rocket!')

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='%prog 0.1.0')

        parser.add_option('-f', '--file', action='store', type='string', dest='file', help='file')

        parser.add_option('-F', '--flag', action='store_true', default=False, help='flag')

        parser.add_option('-v', '--verbose', action='store_true', default=False, help='verbose mode')

        (options, args) = parser.parse_args()

        # if not options.file:
        #     parser.error('missing argument: -f FILE')

        main()
        if options.verbose: print('\n' + time.asctime())
        if options.verbose: print('Total Runtime: ', end='')
        if options.verbose: print(str((time.time() - start_time) * 1000) + ' ms')
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
