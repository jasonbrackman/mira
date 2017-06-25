# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
import maya.OpenMayaUI as mui
from Qt import __binding__


def get_maya_win(module="PySide"):
    """
    get a QMainWindow Object of maya main window
    :param module (optional): string "PySide"(default) or "PyQt4"
    :return main_window: QWidget or QMainWindow object
    """
    prt = mui.MQtUtil.mainWindow()
    if module == "PyQt":
        import sip
        main_window = sip.wrapinstance(long(prt), QObject)
    elif module in ["PySide"]:
        if __binding__ in ["PySide"]:
            import shiboken
        elif __binding__ in ["PySide2"]:
            import shiboken2 as shiboken
        main_window = shiboken.wrapInstance(long(prt), QWidget)
    elif module == "mayaUI":
        main_window = "MayaWindow"
    else:
        raise ValueError('param "module" must be "mayaUI" "PyQt4" or "PySide"')
    return main_window
