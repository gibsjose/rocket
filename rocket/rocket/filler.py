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
        fh, abs_path = tempfile.mkstemp()
        with open(abs_path,'w') as new_file:
            with open(filepath) as old_file:
                # Get header file name
                for f in self.files:
                    regex = re.compile(r'^.+\.h$')
                    if regex.match(f):
                        header = os.path.basename(f)

                for line in old_file:
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

                    # {AUTHORS}
                    elif '{AUTHORS}' in line:
                        first_author = self.configuration.authors[0]
                        auth = first_author['name'];
                        if 'email' in first_author:
                            auth += ' (' + first_author['email'] + ')'

                        new_file.write(line.replace('{AUTHORS}', auth))

                        if len(self.configuration.authors) > 1:
                            auth_iter = iter(self.configuration.authors)
                            next(auth_iter)
                            for author in auth_iter:
                                auth = author['name']
                                if 'email' in author:
                                    auth += ' (' + author['email'] + ')'

                                if self.configuration.language == Language.python:
                                    new_file.write('#\t' + auth + '\n')
                                else:
                                    new_file.write('*\t' + auth + '\n')

                    # {WEBSITES}
                    elif '{WEBSITES}' in line:
                        if len(self.configuration.websites) > 0:
                            new_file.write(line.replace('{WEBSITES}', self.configuration.websites[0]))

                            webs_iter = iter(self.configuration.websites)
                            next(webs_iter)
                            for website in webs_iter:
                                if self.configuration.language == Language.python:
                                    new_file.write('#\t' + website + '\n')
                                else:
                                    new_file.write('*\t' + website + '\n')

                    # Header guards
                    elif '{GUARD}' in line:
                        guard = self.configuration.project.replace(' ', '_').upper() + '_H'
                        new_file.write(line.replace('{GUARD}', guard))

                    # Includes
                    elif '{HEADER}' in line:
                        new_file.write(line.replace('{HEADER}', header))

                    else:
                        new_file.write(line)

        # Close file
        os.close(fh)

        #Remove original file
        os.remove(filepath)

        #Move new file
        shutil.move(abs_path, filepath)

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
        fh, abs_path = tempfile.mkstemp()
        with open(abs_path,'w') as new_file:
            with open(filepath) as old_file:
                for line in old_file:
                    # {BIN}
                    if '{BIN}' in line:
                        new_file.write(line.replace('{BIN}', binary))

                    else:
                        new_file.write(line)

        # Close file
        os.close(fh)

        #Remove original file
        os.remove(filepath)

        #Move new file
        shutil.move(abs_path, filepath)

        print('\t> Configured ' + os.path.basename(filepath))
