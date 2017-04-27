from PySide import QtGui
import get_engine


def get_maya_win(module="mayaUI"):
    import maya.OpenMayaUI as mui
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


def get_nuke_win():
    app = QtGui.qApp
    nuke_win = app.activeWindow()
    return nuke_win


def get_parent_win():
    parent_win = None
    engine = get_engine.get_engine()
    if engine == "maya":
        parent_win = get_maya_win("PySide")
    elif engine == "nuke":
        parent_win = get_nuke_win()
    else:
        # todo
        print "add method to how to get main window."
    return parent_win
