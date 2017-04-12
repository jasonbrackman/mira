# -*- coding: utf-8 -*-

import os
import get_md5


def compile_files(first_file, sec_file):
    if os.path.isfile(first_file) and os.path.isfile(sec_file):
        if get_md5.get_md5(first_file) == get_md5.get_md5(sec_file):
            return True
        return False
    raise ValueError("not a exist file.")
