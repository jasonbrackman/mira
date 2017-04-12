#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import os
import sys


path = __file__
nuke_path = r'C:\tools\Nuke9.0v3\Nuke9.0.exe'


def get_input():
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
        input_file = input_file.replace('\\', '/')
        if os.path.isdir(input_file):
            return input_file
        else:
            print "Please drug a folder"


def get_nuke_path():
    for i in os.listdir('C:/Program Files'):
        if i.startswith('Nuke'):
            nuke_dir = os.path.join('C:/Program Files', i)
            nuke_exe = i.split('v')[0]+'.exe'
            nuke_exe_path = os.path.join(nuke_dir, nuke_exe)
            if os.path.isfile(nuke_exe_path):
                return nuke_exe_path
            else:
                print "%s does not exist" % nuke_exe_path
            break


def main():
    folder = get_input()
    if folder:
        dir_name = os.path.dirname(path)
        py_path = os.path.join(dir_name, 'output_mov.py')
        #nuke_path = get_nuke_path()
        #nuke_path = nuke_path.replace('\\', '/')
        cmd = '"%s" -t %s %s' % (nuke_path, py_path, folder)
        print cmd
        os.system(cmd)


if __name__ == '__main__':
    main()