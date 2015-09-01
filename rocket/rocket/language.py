#!/usr/bin/env python3

#   Rocket - Language
#
#   Joe Gibson (gibsjose@mail.gvsu.edu)
#
#   17 August 2015
#
#   http://gibsjose.com
#   http://github.com/gibsjose/Rocket

from enum import Enum

class Language(Enum):
    """
    Defines the available languages as enumerated types
    """
    unknown = 0
    c = 1
    cpp = 2
    avr_c = 3
    avr_cpp = 4
    python = 5

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
