# -*- coding: utf-8 -*-

import maya.cmds as mc
import maya.mel as mel
from PySide import QtGui
from miraLibs.mayaLibs import get_maya_win


class NormalCopy:
    def __init__(self):
        self.select_list = mc.ls(sl=1, l=1)
        self.load_plugin()

    @staticmethod
    def load_plugin():
        if not mc.pluginInfo('normalCopy', q=1, l=1):
            mc.loadPlugin('normalCopy.mll')

    def do_normal_copy(self):
        if not len(self.select_list) == 2:
            maya_win = get_maya_win.get_maya_win("PySide")
            QtGui.QMessageBox.information(maya_win, 'error', 'select two objects ,please')
            return
        src_obj = self.select_list[0]
        tar_obj = self.select_list[1]
        _cmd = "normalCopy -src \"%s\" -tar \"%s\"" % (src_obj, tar_obj)
        mel.eval(_cmd)


def main():
    op = NormalCopy()
    op.do_normal_copy()

if __name__ == '__main__':
    main()
