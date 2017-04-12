__author__ = 'heshuai'
from PySide import QtGui, QtCore
import maya.cmds as mc
import maya.OpenMayaUI as mui


def get_maya_win():
    import maya.OpenMayaUI as mui
    if 'PyQt4' in QtGui.__name__:
        import sip
        prt = mui.MQtUtil.mainWindow()
        return sip.wrapinstance(long(prt), QtGui.QWidget)
    elif 'PySide' in QtGui.__name__:
        import shiboken
        prt = mui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(prt), QtGui.QWidget)


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
    import shiboken
    panel = mc.getPanel(underPointer=True)
    if not panel:
        return
    ptr = mui.MQtUtil.findControl(panel)
    widget = shiboken.wrapinstance(long(ptr), QtCore.QObject)
    return widget