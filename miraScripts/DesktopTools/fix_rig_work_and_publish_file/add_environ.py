#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_add_environ
# description : ''
# author      : HeShuai
# date        : 2016/1/12
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import sys
import getpass
# Third-party modules

# Studio modules

# Local modules
import get_parent_dir

logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_add_environ_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


parent_dir = get_parent_dir.get_parent_dir()
parent_dir = parent_dir.replace("\\", "/")
sys.path.insert(0, parent_dir)

user = getpass.getuser()
if user == "heshuai":
    script_path = 'E:/aas_repos'
else:
    script_path = 'Z:/Resource/Support/aas_repos'
sys.path.insert(0, script_path)


if __name__ == '__main__':
    pass
