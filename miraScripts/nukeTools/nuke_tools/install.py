#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/11/10
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import getpass
import sys
# Third-party modules

# Studio modules

# Local modules


class Install(object):
    def __init__(self):
        self.user = getpass.getuser()

    @staticmethod
    def get_os_type():
        if 'win' in sys.platform:
            return 'windows'
        if 'linux' in sys.platform:
            return 'linux'

    def get_plugin_path(self):
        if self.get_os_type() == 'windows':
            if self.user == 'heshuai':
                script_path = 'E:/mira/miraScripts/nukeTools/nuke_tools/scripts'
            else:
                script_path = 'Z:/mira/miraScripts/nukeTools/nuke_tools/scripts'
            return script_path

    def install(self):
        target_path = r'C:\Users\%s\.nuke\menu.py' % self.user
        if not os.path.isfile(target_path):
            f = open(target_path, 'w')
            f.close()
        with open(target_path, 'a') as f:
            script_path = self.get_plugin_path()
            new_text = "\n\nnuke.pluginAddPath(\"%s\")" % script_path
            f.write(new_text)

if __name__ == '__main__':
    ins = Install()
    ins.install()
