__author__ = 'heshuai'

import sys


def get_os_type():
    if sys.platform.startswith('win'):
        os_type = 'windows'
    elif sys.platform.startswith('linux'):
        os_type = 'linux'
    else:
        os_type = 'mac'
    return os_type