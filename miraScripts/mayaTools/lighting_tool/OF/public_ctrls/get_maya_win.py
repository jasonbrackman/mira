__author__ = 'heshuai'
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from Qt import __binding__
import maya.cmds as mc
import maya.OpenMayaUI as mui


def get_maya_win(module="PySide"):
    """
    get a QMainWindow Object of maya main window
    :param module (optional): string "PySide"(default) or "PyQt4"
    :return main_window: QWidget or QMainWindow object
    """
    import maya.OpenMayaUI as mui
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


def get_maya_main_win_pos():
    main_window = get_maya_win()
    for i in main_window.children():
        if i.objectName() == 'formLayout1':
            view_pos = main_window.mapToGlobal(i.pos())
            return [view_pos.x(), view_pos.y()]


def get_maya_main_win_size():
    main_window = get_maya_win()
    for i in main_window.children():
        if i.objectName() == 'formLayout1':
            view_size = i.size()
            return [view_size.width(), view_size.height()]


def get_widget_under_pointer():
    try:
        import shiboken
    except:
        import shiboken2 as shiboken
    panel = mc.getPanel(underPointer=True)
    if not panel:
        return
    ptr = mui.MQtUtil.findControl(panel)
    widget = shiboken.wrapinstance(long(ptr), QObject)
    return widget