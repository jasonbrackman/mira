# -*- coding: utf-8 -*-
import maya.OpenMayaUI as mui


def get_maya_win(module="mayaUI"):
    """
    get a QMainWindow Object of maya main window
    :param module (optional): string "PySide"(default) or "PyQt4"
    :return main_window: QWidget or QMainWindow object
    """
    prt = mui.MQtUtil.mainWindow()
    if module == "PyQt4":
        import sip
        import PyQt4.QtCore as QtCore
        main_window = sip.wrapinstance(long(prt), QtCore.QObject)
    elif module == "PySide":
        import shiboken
        import PySide.QtGui as QtGui
        main_window = shiboken.wrapInstance(long(prt), QtGui.QWidget)
    elif module == "mayaUI":
        main_window = "MayaWindow"
    else:
        raise ValueError('param "module" must be "mayaUI" "PyQt4" or "PySide"')
    return main_window
