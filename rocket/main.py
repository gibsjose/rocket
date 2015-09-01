#!/usr/bin/env python3

#   Rocket
#
#   Joe Gibson (gibsjose@mail.gvsu.edu)
#
#   17 August 2015
#
#   http://gibsjose.com
#   http://github.com/gibsjose/Rocket

# @TODO Look into using inflection library for camel-case, etc. https://inflection.readthedocs.org/en/latest/
#       Inflection will solve the bug where naming projects certain ways results in their naming being incorrect
# @TODO Make the `extension` attribute for Python have a local override in `config.json` to more easily decide on using `.py` extension
# @TODO ^^^^^ Maybe there is a `config.json` in each language folder??? Probably best!
# @TODO Add support for {DATE} formatting... i.e. '{DD MONTH YYYY}' or '{MM.DD.YYYY}', etc.
# @TODO FIX: When there are no `websites` or `license` specified, there is an extra line in the comment header...
# @TODO Add support for either Python 2 or 3
# @TODO Add an `simple` T/F attribute to Python config.json. Use current structure, etc. when True, otherwise use the project structure used for Rocket...

# Essential Modules
from enum import Enum
import sys
import os
import traceback
import argparse
import re
import operator
import time
import datetime
import tempfile
import stat
import glob

# Other Modules
import json         # JSON
import shutil       # File Copying, `which()`, etc.
import subprocess   # Call shell commands for `git`

# Local Modules
from rocket.language import Language
import rocket.language
import rocket.configuration
import rocket.filler
import rocket.namer

# Global language dictionary
LanguageDictionary = {
    'c': Language.c,
    'cpp': Language.cpp,
    'c++': Language.cpp,
    'avr-c': Language.avr_c,
    'avr-cpp': Language.avr_cpp,
    'avr-c++': Language.avr_cpp,
    'python': Language.python
}

# Matches language names with their template directory name
LanguageNameDictionary = {
    'c': 'c',
    'cpp': 'cpp',
    'c++': 'cpp',
    'avr-c': 'avr-c',
    'avr-cpp': 'avr-cpp',
    'avr-c++': 'avr-cpp',
    'python': 'python'
}

class Rocket:
    """
    Defines the Rocket object for creating project/code templates
    """
    def __init__(self):
        """
        Rocket default constructor
        """
        self.language = Language.unknown
        self.dir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

    def Create(self, language, project):
        """
        Generates the skeleton code, makefiles (if necessary), gitignore
        files, etc. and generates a default `config.json` object with the correct language
        """
        # Set language
        # - 'language' is the user's raw input
        # - 'lang' is a lowercase version of 'language'
        # - 'self.language' is the actual language type enum (e.g. Language.cpp)
        # - 'language_name' is the accepted language name by Rocket (e.g. 'C++' turn to 'cpp')
        lang = language.lower()
        if lang in LanguageDictionary:
            self.language = LanguageDictionary[lang]
            language_name = LanguageNameDictionary[lang]
        else:
            self.language = Language.unknown
            language_name = 'unknown'
            raise Exception('Unknown language')

        print('\t> Copying from Rocket directory: ' + self.dir)

        # Pull correct files and copy them to local directory
        directory = os.getcwd()
        print('\t> Current directory: ' + directory)

        # Write a default `config.json` file with the correct language
        # Read in the default file, change the language attribute, and write it
        self.configuration = rocket.configuration.Configuration()
        self.configuration.Modify(self.dir + '/config.json', directory + '/config.json', language_name, project)
        print('\t> Created default ' + language + ' configuration file \'./config.json\'')

        # @TODO Make this more modular by using the language's 'language.json' file and a LanguageConfiguration object
        # Make directories and copy files as needed for specific languages
        if (self.language == Language.c) or (self.language == Language.cpp) or (self.language == Language.avr_c) or (self.language == Language.avr_cpp):
            # Create necessary directories
            if not os.path.exists(directory + '/src/'):
                os.makedirs(directory + '/src/')
                print('\t> Created source directory \'./src/\'')

            # Copy the skeleton code
            if (self.language == Language.c) or (self.language == Language.avr_c):
                shutil.copy(self.dir + '/languages/' + language_name + '/skeleton/rocket.c', directory + '/src/')
                shutil.copy(self.dir + '/languages/' + language_name + '/skeleton/rocket.h', directory + '/src/')
                print('\t> Created skeleton \'.c\' and \'.h\' files in \'./src/\'')
            else:
                shutil.copy(self.dir + '/languages/' + language_name + '/skeleton/rocket.cpp', directory + '/src/')
                shutil.copy(self.dir + '/languages/' + language_name + '/skeleton/rocket.h', directory + '/src/')
                print('\t> Created skeleton \'.cpp\' and \'.h\' files in \'./src/\'')

            # Copy the makefile
            shutil.copy(self.dir + '/languages/' + language_name + '/makefile', directory)
            print('\t> Created ' + language + ' \'./makefile\'')

        elif self.language == Language.python:
            shutil.copy(self.dir + '/languages/' + language_name + '/skeleton/rocket.py', directory)
            print('\t> Created skeleton \'.py\' file')

    def Config(self):
        """
        Pull from the generated and (maybe) edited `config.json` file, and
        make changes to comment header blocks
        """
        # Create a configuration object
        self.configuration = rocket.configuration.Configuration()

        # Decode the configuration object
        self.configuration.Decode(os.getcwd() + '/config.json')

        if self.configuration.language_string in LanguageNameDictionary:
            language_name = LanguageNameDictionary[self.configuration.language_string]
        else:
            language_name = 'unknown'

        print('\t> Generated date: ' + self.configuration.date)
        print('\t> Detected language: ' + self.configuration.language_string)
        print('\t> Detected project name: ' + self.configuration.project)

        # Modify skeleton files/makefiles with data from `config.json`
        directory = os.getcwd()

        # Rename skeleton code files to project name
        file_namer = rocket.namer.FileNamer(self.configuration, self.dir)
        files = file_namer.Rename()

        # Modify skeleton code (and makefile if necessary)
        comment_filler = rocket.filler.CommentFiller(self.configuration)
        comment_filler.Replace(files)

        makefile_filler = rocket.filler.MakefileFiller(self.configuration)
        makefile_filler.Replace(directory + '/makefile', file_namer.name)

        # Re-apply executable privilages for Python scripts
        if self.configuration.language == Language.python:
            for f in files:
                os.chmod(f, stat.S_IRWXU)

        # If project will be a `git` repo add `.gitignore` and `README.md`
        if self.configuration.git:
            # Create README
            with open(directory + '/README.md', 'w') as readme:
                readme.write('# ' + self.configuration.project + '\n')
                readme.write(self.configuration.date + '\n')
                # @TODO Write license/other info here

            # Copy the `.gitignore`
            shutil.copy(self.dir + '/languages/' + language_name + '/' + language_name + '.gitignore', directory + '/.gitignore')
            print('\t> Created ' + self.configuration.language_string + ' \'./.gitignore\'')

            # Add executable name to .gitignore for non-Python projects
            if not self.configuration.language == Language.python:
                with open(directory + '/.gitignore', 'a') as gi:
                    gi.write('\n# Actual binary\n')
                    gi.write(file_namer.name)

            # Run `git init`
            out = subprocess.check_output("git init", shell=True, universal_newlines=True)
            print('\t> ' + str(out), end='')

        # Set `origin` and set to push refs
        if self.configuration.git and self.configuration.git_remote:
            try:
                out = subprocess.check_output('git remote add origin ' + self.configuration.git_remote, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)

                try:
                    # Call this and discard output to ensure the remote was added properly
                    subprocess.check_output('git remote show origin', stderr=subprocess.STDOUT, shell=True, universal_newlines=True)

                    # Use this output (it is much cleaner) for displaying remote name
                    out = subprocess.check_output('git config --get remote.origin.url', shell=True, universal_newlines=True)
                    print('\t> git remote origin: ' + str(out), end='')

                    if self.configuration.git_push:
                        try:
                            # Add files
                            subprocess.check_output('git add .', shell=True, universal_newlines=True)

                            # Initial commit
                            subprocess.check_output('git commit -m \'Inital commit\'', shell=True, universal_newlines=True)

                            # Push
                            out = subprocess.check_output('git push -u origin master', stderr=subprocess.STDOUT, shell=True, universal_newlines=True)

                            print('\t> ' + str(out).replace('\n', '\n\t  '), end='')

                            # Show commit object hash
                            out = subprocess.check_output('git log --pretty=format:\'%h\' -n 1', shell=True, universal_newlines=True)

                            print('\n\t> Pushed initial commit ' + str(out).replace('\n', '...'))

                        except subprocess.CalledProcessError as e:
                            print('\t! Unable to push initial commit:\n\t  ' + e.output.replace('\n', '\n\t  '))

                except subprocess.CalledProcessError as e:
                    print('\t! Error getting remote:\n\t  ' + e.output.replace('\n', '\n\t  '))

            except subprocess.CalledProcessError as e:
                print('\t! Error adding remote: ' + e.output, end='')
                print('\t! Try running \'rm -rf .git/; rocket config\' to REMOVE ALL GIT FILES and re-configure')

        elif not self.configuration.git and self.configuration.git_remote:
            print('\t! Error: You specified to add a git remote but NOT to create a git repo...')

        elif not self.configuration.git_remote and self.configuration.git_push:
            print('\t* Warning: You configured to \'push\' the git repo but you did not provide a valid repo...')

    def Clean(self):
        """
        Remove generated project files in the current directory
        """
        directory = os.getcwd()

        # Make sure user knows exactly which directory they are in
        response = input('Remove all project files in \'' + directory + '\'? [Y/n]: ')
        if not response == 'Y':
            return 1

        # Have at least *some* sanity check...
        if directory == self.dir:
            raise Exception('Removing here would remove Rocket\'s files...')
        elif directory == '/':
            raise Exception('You do not really want to remove \'' + directory + '\', right...?')
        elif directory == '/usr':
            raise Exception('You do not really want to remove \'' + directory + '\', right...?')
        elif directory == os.path.expanduser('~'):
            raise Exception('You do not really want to remove \'' + directory + '\', right...?')

        # Can use the `config.json` to more intelligently remove files if it exists
        if os.path.exists(directory + '/config.json'):
            configuration = rocket.configuration.Configuration()
            configuration.Decode(directory + '/config.json')
            configuration.Print()

        # @TODO Add 'files' attribute to 'config.json' when generating as files are added and only use that! Do not do any blind removal

        # @TODO How to handle '.gitignore' and '.git/'?

        # Else do blind removal of *.py, config.json, makefile, .gitignore, ./.git/, ./src/, ./obj/, ./bin/, {Executable}, etc.
        # else:
        #     os.remove(glob(directory + '/*.py'))
        #     os.remove(directory + '/config.json')
        #     os.remove(directory + '/makefile')
        #     os.remove(directory + '/.gitignore')
        #     shutil.rmtree(directory + '/.git/')
        #     shutil.rmtree(directory + '/src/')
        #     shutil.rmtree(directory + '/obj/')
        #     shutil.rmtree(directory + '/bin/')

        return 0

    def Print(self):
        """
        Prints the configuration data in a nice format
        """
        self.configuration.Print()

def main():
    """
    Rocket main
    """
    global args

    print('-------')
    print('Rocket!')
    print('-------')

    # Make sure Rocket is not being executed in the install directory
    if os.getcwd() == os.path.dirname(os.path.realpath(sys.argv[0])):
        raise Exception('You do not want to execute \'rocket\' in it\'s own directory...')

    # Execute command
    if args.command == 'clean':
        directory = os.getcwd()
        print('\n>>> Removing existing project files >>>')
        rocket = Rocket()
        if not rocket.Clean():
            print('<<< Project files removed <<<\n')

    elif args.command == 'create':
        print('\n>>> Creating a blank ' + args.language + ' project named \'' + args.project + '\' >>>')

        path, dirname = os.path.split(os.getcwd())

        # Directory already has project name
        if args.project == dirname:
            #Non-empty named directory: Prompt user
            if os.listdir(os.getcwd()):
                if not input('You really should run \'rocket create\' in an empty directory... Continue? [Y/n] ') == 'Y':
                    return 0

        # Directory has different name
        else:
            # Make directory named after project and enter it
            os.makedirs(args.project)
            os.chdir(args.project)
            print('\t> Created project directory: \'' + os.path.dirname(os.getcwd() + '/') + '\'')

        rocket = Rocket()
        rocket.Create(args.language, args.project)
        print('<<< Created skeleton ' + args.language + ' project <<<')
        print('<<< Edit the \'config.json\' file with your project settings and run \'rocket config\' to finish <<<\n')

    elif args.command == 'config':
        rocket = Rocket()
        print('\n>>> Configuring the project >>>')
        rocket.Config()
        print('<<< Configured \'' + rocket.configuration.project + '\' <<<\n')

    else:
        raise Exception('Must specify language with \'-l LANGUAGE\' or run config with \'-c\' or \'--config\'')

if __name__ == '__main__':
    try:
        start_time = time.time()

        parser = argparse.ArgumentParser(prog='rocket', description='generate a base project in C, C++, or Python')

        # Options
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose mode')

        # Commands
        subparsers = parser.add_subparsers(help='commands:', dest='command')

        create_parser = subparsers.add_parser('create', help='create a new project')
        create_parser.add_argument('project', help='project name')
        create_parser.add_argument('language', type=str.lower, help='project language', choices=['c', 'c++', 'cpp', 'python'])

        config_parser = subparsers.add_parser('config', help='configure a project')

        clean_parser  = subparsers.add_parser('clean', help='remove all project files')

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
        print('\n<-- Exception: ', end='')
        print(str(e), end=' -->\n\n')
        if(args.verbose):
            traceback.print_exc()

        os._exit(1)
