# -*- coding: utf-8 -*-
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
        from Qt.QtCore import *
        main_window = sip.wrapinstance(long(prt), QObject)
    elif module in ["PySide", "PyQt"]:
        if __binding__ in ["PySide", "PyQt4"]:
            import shiboken
        elif __binding__ in ["PySide2", "PyQt5"]:
            import shiboken2 as shiboken
        from Qt.QtWidgets import *
        main_window = shiboken.wrapInstance(long(prt), QWidget)
    elif module == "mayaUI":
        main_window = "MayaWindow"
    else:
        raise ValueError('param "module" must be "mayaUI" "PyQt4" or "PySide"')
    return main_window
