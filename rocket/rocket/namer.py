#!/usr/bin/env python3

#   Rocket - Namer
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
import tempfile
import stat

# Other Modules
import shutil       # File Copying, `which()`, etc.

# Local Modules
from rocket.language import Language
import rocket.configuration

class FileNamer:
    """
    Renames files with appropriate name
    """
    def __init__(self, configuration, r_dir):
        """
        Sets configuration values and parses language config, if it exists
        """
        self.configuration = configuration

        self.dir = r_dir
        language_file = self.dir + '/languages/' + self.configuration.language_name + '/language.json'

        self.language_configuration = rocket.configuration.LanguageConfiguration()
        self.language_configuration.Decode(language_file)

    def SpacesToUnderscores(self, word):
        """
        Converts spaces to lowercase underscores: 'Rocket Project' -> 'rocket_project'
        """
        return word.replace(' ', '_').lower()

    def SpacesToDashes(self, word):
        """
        Converts spaces to lowercase dashes: 'Rocket Project' -> 'rocket-project'
        """
        return word.replace(' ', '-').lower()

    def UnderscoresToCamelCase(self, word):
        """
        Converts lowercase underscores to CamelCase: 'rocket_project' -> 'RocketProject'
        """
        return ''.join(x.capitalize() or '_' for x in word.split('_'))

    def SpacesToCamelCase(self, word):
        """
        Converts spaces to CamelCase: 'Rocket Project' -> 'RocketProject'
        """
        return self.UnderscoresToCamelCase(self.SpacesToUnderscores(word))

    def GenerateName(self):
        """
        Generates a name for a file based on the project name and language type
        """
        # First try to pull from the $(ROCKET_DIR)/languages/*/language.json file
        if self.language_configuration.exists:
            # Naming options:
            #   'dashes' or 'dash': 'Rocket Project' -> 'rocket-project'
            #   'underscores' or 'underscore': 'Rocket Project' -> 'rocket_project'
            #   'camel-case' or 'camelcase' or 'camel_case': 'Rocket Project' -> 'RocketProject'
            naming = self.language_configuration.naming
            print('\t> Using naming: ' + naming)

            if naming == 'dashes' or naming == 'dash':
                self.name = self.SpacesToDashes(self.configuration.project)
                return

            elif naming == 'underscores' or naming == 'underscore':
                self.name = self.SpacesToUnderscores(self.configuration.project)
                return

            elif naming == 'camel-case' or naming == 'camelcase' or naming == 'camel_case':
                self.name = self.SpacesToCamelCase(self.configuration.project)
                return

            # If 'naming' attribute unrecognized, just break and use defaults below
            else:
                None;

        # Otherwise use defaults
        language = self.configuration.language

        # 'Rocket Project' -> 'rocket-project' for C
        if language == Language.c or language == Language.avr_c:
            self.name =  self.SpacesToDashes(self.configuration.project)
            print('\t> Defaulting to \'dashes\' naming for ' + self.configuration.language_string + ' projects')

        # 'Rocket Project' -> 'RocketProject' for C++
        elif language == Language.cpp or language == Language.avr_cpp:
            self.name = self.SpacesToCamelCase(self.configuration.project)
            print('\t> Defaulting to \'camel-case\' naming for ' + self.configuration.language_string + ' projects')

        # 'Rocket Project' -> 'rocket_project' for Python
        elif language == Language.python:
            self.name =  self.SpacesToUnderscores(self.configuration.project)
            print('\t> Defaulting to \'underscores\' naming for ' + self.configuration.language_string + ' projects')

        # 'Rocket Project' -> 'rocket_project' for all else
        else:
            self.name = self.SpacesToUnderscores(self.configuration.project)
            print('\t> Defaulting to \'underscores\' naming for ' + self.configuration.language_string + ' projects')

        return

    def Rename(self):
        """
        Rename the files according to the project name
        """
        # Generate a name
        self.GenerateName()
        print('\t> Name generated: ' + self.name)

        # Create file list
        self.files = []
        language = self.configuration.language
        sources = self.language_configuration.sources

        directory = os.getcwd()

        if language == Language.python:
            src_directory = directory + '/'
        else:
            src_directory = directory + '/src/'

        for f in os.listdir(src_directory):
            for s in sources:
                if f.endswith(s):
                    self.files.append(src_directory + f)

        # print('\t> Renaming the following files:')
        # for f in self.files:
        #     print('\t\t* ' + os.path.basename(f))

        # Rename all files
        self.renamed = []
        for f in self.files:
            self.renamed.append(self.RenameFile(f))

        # print('\t> to:')
        # for f in self.renamed:
        #     print('\t\t* ' + os.path.basename(f))

        return self.renamed

    def RenameFile(self, filepath):
        """
        Rename an individual file according to the project name
        """
        new_name = filepath.replace('rocket', self.name)

        if not self.language_configuration.extension:
            for s in self.language_configuration.sources:
                print('\t> Dropping \'' + s + '\' extension')
                new_name = new_name.replace(s, '')

        os.rename(filepath, new_name)

        return new_name
