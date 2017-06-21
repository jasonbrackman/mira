#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import os
import sys
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *

path = __file__
nuke_path = r'C:\tools\Nuke9.0v3\Nuke9.0.exe'

fps_list = ['24', '25']


def get_fps():
    QApplication(sys.argv)
    ret_value = QInputDialog.getItem(None, 'choose fps', 'Please choose fps...', fps_list)
    value, ok = ret_value
    if ok:
        return value


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
    fps = get_fps()
    if not folder:
        return
    if not fps:
        return
    dir_name = os.path.dirname(path)
    py_path = os.path.join(dir_name, 'output_mov.py')
    # nuke_path = get_nuke_path()
    # nuke_path = nuke_path.replace('\\', '/')
    cmd = '"%s" -t %s %s %s' % (nuke_path, py_path, folder, fps)
    print cmd
    os.system(cmd)


if __name__ == '__main__':
    main()
