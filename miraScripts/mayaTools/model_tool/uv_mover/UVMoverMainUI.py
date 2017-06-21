#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_UVMoverMainUI
# description : ''
# author      : Aaron Hui
# date        : 20step6/3/step6
# version     :
# usage       :
# notes       :

# Built-in modules
import logging
import os
# Third-party modules
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
import pymel.core as pm

# Studio modules

# Local modules
import uv_mover
from miraLibs.mayaLibs import get_maya_win


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_UVMoverMainUI_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class UVMoverMainUI(QDialog):

    def __init__(self, parent=None):
        super(UVMoverMainUI, self).__init__(parent)

        self.setFocus()
        self._ui = uv_mover.Ui_UVMover()
        self._ui.setupUi(self)
        self._history = []

    def do_move_uv(self):
        # get step
        step = 1
        # get direction
        clicked_btn = self.sender()
        btn_name = clicked_btn.objectName()
        direction_dict = {"l_up_btn": {"uValue": -step, "vValue": step},
                          "up_btn": {"vValue": step},
                          "r_up_btn": {"uValue": step, "vValue": step},
                          "left_btn": {"uValue": -step},
                          "right_btn": {"uValue": step},
                          "l_down_btn": {"uValue": -step, "vValue": -step},
                          "down_btn": {"vValue": -step},
                          "r_down_btn": {"uValue": step, "vValue": -step},
                          }
        # select uv of selection objects
        pm.mel.eval("PolySelectConvert 4")
        # do move
        pm.polyEditUVShell(**direction_dict[btn_name])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self._ui.up_btn.clicked.emit()
        if event.key() == Qt.Key_Left:
            self._ui.left_btn.clicked.emit()
        if event.key() == Qt.Key_Right:
            self._ui.right_btn.clicked.emit()
        if event.key() == Qt.Key_Down:
            self._ui.down_btn.clicked.emit()


def main():
    wgt = UVMoverMainUI(get_maya_win.get_maya_win("PySide"))
    wgt.show()


if __name__ == "__main__":
    main()
