# -*- coding: utf-8 -*-
import os
import shiboken
from PySide import QtGui
from input import Input
from output import Output
from asset_pool_libs.get_engine import get_engine


class AssetPool(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AssetPool, self).__init__(parent)
        self.setObjectName("Asset Pool")
        self.resize(380, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        tab_widget = QtGui.QTabWidget()
        tab_widget.setTabPosition(QtGui.QTabWidget.West)

        input_pool = Input()
        output_pool = Output()
        tab_widget.addTab(input_pool, "Input")
        tab_widget.addTab(output_pool, "Output")

        main_layout.addWidget(tab_widget)


def create_dock(docked=True):
    import maya.OpenMayaUI as mui
    import maya.cmds as mc
    dialog = AssetPool()
    if docked:
        ptr = mui.MQtUtil.mainWindow()
        main_window = shiboken.wrapInstance(long(ptr), QtGui.QWidget)
        dialog.setParent(main_window)
        size = dialog.size()
        name = mui.MQtUtil.fullName(long(shiboken.getCppPointer(dialog)[0]))
        dock = mc.dockControl(
            allowedArea=['right', 'left'],
            area='left',
            floating=False,
            content=name,
            width=size.width(),
            height=size.height(),
            label='Asset Pool')
        return dock
    else:
        dialog.show()


def show_in_maya():
    import maya.utils as mu
    import maya.cmds as mc
    global dock_widget
    try:
        mc.deleteUI(dock_widget)
    except:pass
    dock_widget = create_dock(True)
    mu.executeDeferred("mc.dockControl(\"%s\", e=1, r=1)" % dock_widget)


def main():
    engine = get_engine()
    if engine == "maya":
        show_in_maya()
