# -*- coding: utf-8 -*-
try:
    from PySide import QtGui
except:
    from PyQt4 import QtGui
import maya.cmds as mc
import get_maya_win


def delete_last(widget_class):
    class WrapperClass(widget_class):
        def __init__(self, *args, **kwargs):
            widget_class.__init__(self, *args, **kwargs)
            if not self.objectName():
                object_name = "@OBJECTNAME@"
                self.setObjectName(object_name)

        @classmethod
        def show_ui(cls, *args, **kwargs):
            obj = cls(*args, **kwargs)
            object_name = obj.objectName()
            while 1:
                if mc.window(object_name, q=1, ex=1):
                    mc.deleteUI(object_name)
                else:
                    break
            model = QtGui.__name__.split(".")[0]
            ui = cls(get_maya_win.get_maya_win(model), *args, **kwargs)
            ui.show()
    return WrapperClass


def show_ui(widget_class, *args, **kwargs):
    ui = delete_last(widget_class)()
    ui.show_ui(*args, **kwargs)
