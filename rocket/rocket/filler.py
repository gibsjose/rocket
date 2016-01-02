#!/usr/bin/env python3

#   Rocket - Filler
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
import shutil

# Local Modules
from rocket.language import Language
import rocket.configuration

class CommentFiller:
    """
    Replaces comment blocks in files with the appropriate data
    """
    def __init__(self, configuration):
        """
        Sets configuration values
        """
        self.configuration = configuration

    def Replace(self, files):
        """
        Intelligently replace comments in files based on language type
        """
        self.files = files

        for f in self.files:
            self.ReplaceInFile(f)

    def ReplaceInFile(self, filepath):
        """
        Replace the comment tags with actual data in a source file
        """
        if not os.path.exists(filepath):
            raise Exception('Cannot modify \'' + filepath + '\': Does not exist')

        #Create temp file
        new_fh, new_path = tempfile.mkstemp()
        with open(new_path,'w') as new_file:
            with open(filepath, 'r+') as old_file:
                # Get header file name
                for f in self.files:
                    regex = re.compile(r'^.+\.h$')
                    if regex.match(f):
                        header = os.path.basename(f)

                # First make as many lines as are needed for the authors/websites/etc. in a temp file
                temp_fh, temp_path = tempfile.mkstemp()
                with open(temp_path,'w') as temp_file:
                    for line in old_file:
                        if ('{AUTHOR-NAME}' in line) or ('{AUTHOR-EMAIL}' in line):
                            for author in self.configuration.authors:
                                temp_file.write(line)
                        elif '{WEBSITE}' in line:
                            for website in self.configuration.websites:
                                temp_file.write(line)
                        elif '{LICENSE}':
                            if self.configuration.license or self.configuration.license_url:
                                temp_file.write(line)
                        else:
                            temp_file.write(line)

                    author_index = 0
                    website_index = 0

                with open(temp_path,'r') as temp_file:
                    for line in temp_file:
                        # {TITLE}
                        if '{TITLE}' in line:
                            new_file.write(line.replace('{TITLE}', self.configuration.project))

                        # {DD MONTH YYYY}
                        elif '{DD MONTH YYYY}' in line:
                            new_file.write(line.replace('{DD MONTH YYYY}', self.configuration.date))

                        # {LICENSE}
                        elif '{LICENSE}' in line:
                            license = 'License: '

                            if self.configuration.license:
                                if not self.configuration.license_url:
                                    license += self.configuration.license
                                else:
                                    license += self.configuration.license + ' ('

                            if self.configuration.license_url:
                                if not self.configuration.license:
                                    license += self.configuration.license_url
                                else:
                                    license += self.configuration.license_url + ')'

                            if self.configuration.license or self.configuration.license_url:
                                new_file.write(line.replace('{LICENSE}', license))

                        # {AUTHOR-NAME} and {AUTHOR-EMAIL}
                        elif '{AUTHOR-NAME}' in line or '{AUTHOR-EMAIL}' in line:
                            auth = self.configuration.authors[author_index]
                            auth_name = auth['name'];
                            if 'email' in auth:
                                auth_email = auth['email']
                            else:
                                auth_email = ''

                            new_line = line.replace('{AUTHOR-NAME}', auth_name)
                            new_line = new_line.replace('{AUTHOR-EMAIL}', auth_email)

                            new_file.write(new_line)

                            author_index += 1

                        elif '{DESCRIPTION}' in line:
                            description = self.configuration.description
                            
                            if description:
                                new_file.write(line.replace('{DECRIPTION}', description))

                        # {WEBSITE}
                        elif '{WEBSITE}' in line:
                            website = self.configuration.websites[website_index]
                            new_file.write(line.replace('{WEBSITE}', website))

                            website_index += 1

                        # Header guards
                        elif '{GUARD}' in line:
                            guard = self.configuration.project.replace(' ', '_').upper() + '_H'
                            new_file.write(line.replace('{GUARD}', guard))

                        # Includes
                        elif '{HEADER}' in line:
                            new_file.write(line.replace('{HEADER}', header))

                        # Write all other lines as they are
                        else:
                            new_file.write(line)

        #Remove original file
        os.remove(filepath)

        #Move new file
        shutil.move(new_path, filepath)

        print('\t> Configured ' + os.path.basename(filepath))

class MakefileFiller:
    """
    Replaces items in makefiles with appropriate data
    """
    def __init__(self, configuration):
        """
        Sets configuration values
        """
        self.configuration = configuration

    def Replace(self, filepath, binary):
        """
        Replace the makefile variables with actual data
        """
        if self.configuration.language == Language.python:
            return

        if not os.path.exists(filepath):
            raise Exception('Cannot modify \'' + filepath + '\': Does not exist')

        #Create temp file
        new_fh, new_path = tempfile.mkstemp()
        with open(new_path,'w') as new_file:
            with open(filepath) as old_file:
                for line in old_file:
                    # {BIN}
                    if '{BIN}' in line:
                        new_file.write(line.replace('{BIN}', binary))

                    else:
                        new_file.write(line)

        #Remove original file
        os.remove(filepath)

        #Move new file
        shutil.move(new_path, filepath)

        print('\t> Configured ' + os.path.basename(filepath))
