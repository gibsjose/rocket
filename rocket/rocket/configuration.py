#!/usr/bin/env python3

#   Rocket - Configuration
#
#   Joe Gibson (gibsjose@mail.gvsu.edu)
#
#   17 August 2015
#
#   http://gibsjose.com
#   http://github.com/gibsjose/Rocket

# Essential Modules
import sys
import os
import re
import operator
import time
import datetime

# Other Modules
import json         # JSON
import shutil       # File Copying, `which()`, etc.
import subprocess   # Call shell commands for `git`

# Local Modules
from rocket.language import Language
import rocket.language

class LanguageConfiguration:
    """
    Language Configuration from a `language.json` file
    """
    def __init__(self):
        """
        Default constructor
        """
        self.data = {}
        self.exists = False
        self.naming = None
        self.sources = []
        self.extension = True

    def Decode(self, filepath):
        """
        Try to read in and parse language config file
        """
        if os.path.exists(filepath):
            self.exists = True

            # Read language JSON data
            with open(filepath, encoding='utf-8') as lang_file:
                # Load JSON data
                self.data = json.loads(lang_file.read())

                # Naming
                if 'naming' in self.data:
                    self.naming = self.data['naming'].replace(' ', '-').lower()
                else:
                    self.naming = None

                # Sources
                if 'sources' in self.data:
                    self.sources = self.data['sources']
                else:
                    self.sources = []

                # extension
                if 'extension' in self.data:
                    self.extension = self.data['extension']
                else:
                    self.extension = True

        else:
            self.exists = False
            self.naming = None
            self.sources = []
            self.extension = True

class Configuration:
    def __init__(self):
        """
        Default constructor
        """
        self.data = {}

    def Modify(self, in_file, out_file, language_string, project):
        """
        Read in the JSON `in_file`, modify the language and project attributes, and write it out as the JSON `out_file`
        """
        # Check if config file exists
        if not os.path.exists(in_file):
            raise Exception('Configuration file does not exist at ' + in_file)

        with open(in_file, encoding='utf-8') as in_fp:
            # Load JSON data
            self.data = json.loads(in_fp.read())

            # Modify language string
            self.data['language'] = language_string

            # Modify project string
            self.data['project'] = project

        with open(out_file, 'w', encoding='utf-8') as out_fp:
            # Write JSON data
            json.dump(self.data, out_fp, sort_keys=True, indent=4)

    def Encode(self, filepath):
        """
        Encode the configuration data as a JSON file
        """
        with open(filepath, 'w', encoding='utf-8') as config_file:
            json.dump(self.data, config_file, sort_keys=True, indent=4)

    def Decode(self, filepath):
        """
        Decode the configuration file as a Python JSON object (dictionary)
        """
        # Get current date in `DD MONTH YYYY` format
        today = datetime.date.today()
        self.date = today.strftime('%d %b %Y')

        # Check if config file exists
        if not os.path.exists(filepath):
            raise Exception('Configuration file does not exist at ' + filepath)

        # Read config JSON data
        with open(filepath, encoding='utf-8') as config_file:
            # Load JSON data
            self.data = json.loads(config_file.read())

            # Language (string)
            if 'language' not in self.data:
                raise Exception('Must specify \'language\' in config file')

            self.language_string = self.data['language']

            # Language (enum)
            lang = self.language_string.lower()
            if lang in rocket.language.LanguageDictionary:
                self.language = rocket.language.LanguageDictionary[lang]
            else:
                self.language = Language.unknown
                raise Exception('Unknown language')

            # Language (official name)
            self.language_name = rocket.language.LanguageNameDictionary[self.language_string]

            # Project name
            if 'project' not in self.data:
                raise Exception('Must specify \'project\' in config file')
            self.project = self.data['project']

            # Authors
            if 'authors' not in self.data:
                raise Exception('Must specify at least one author under \'authors\' in config file')
            self.authors = self.data['authors']

            for author in self.authors:
                if 'name' not in author:
                    raise Exception('Authors must have \'name\' attribute')

            # Websites
            if 'websites' in self.data:
                self.websites = self.data['websites']
            else:
                self.website = []

            # License
            if 'license' in self.data:
                self.license = self.data['license']
            else:
                self.license = None

            # License URL
            if 'license-url' in self.data:
                self.license_url = self.data['license-url']
            else:
                self.license_url = None

            # Git
            if 'git' in self.data:
                self.git = self.data['git']
            else:
                self.git = False

            # GitHub
            if 'git-push' in self.data:
                self.git_push = self.data['git-push']
            else:
                self.git_push = None

            if 'git-remote' in self.data:
                self.git_remote = self.data['git-remote']
            else:
                self.git_remote = None

    def Print(self):
        print('Project: ' + self.project)
        print('Language: ' + self.language_string)
        print('Date: ' + self.date)
        print('License: ' + self.license)
        print('Author(s):')
        for author in self.authors:
            print('\t' + author['name'], end='')
            if 'email' in author:
                print(': ' + author['email'])
            else:
                print('')
        print('Website(s):')
        if len(self.websites) == 0:
            print('\t None')
        else:
            for website in self.websites:
                print('\t' + website)
        print('Git: ' + str(self.git))
        print('Create GitHub Repo: ' + str(self.git_create))
        print('GitHub Remote: ' + self.git_remote)
        print('GitHub User: ' + self.git_user)
