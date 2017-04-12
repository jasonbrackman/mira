#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_get_python_path
# description : ''
# author      : HeShuai
# date        : 2016/1/14
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import getpass
# Third-party modules

# Studio modules

# Local modules


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_get_python_path_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def get_python_path():
    user = getpass.getuser()
    if user == "heshuai":
        python_path = 'python'
    else:
        python_path = 'Z:\Resource\Pipeline\app_config\system\wrappers\python_tank.bat'
    return python_path


if __name__ == "__main__":
    pass
