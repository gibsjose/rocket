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
