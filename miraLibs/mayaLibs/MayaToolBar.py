# -*- coding: utf-8 -*-
import logging
import maya.OpenMayaUI as om
import shiboken
from PySide import QtGui


class MayaToolBar(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tool_bar_layout = None
        self.get_tool_bar_layout()

    def get_tool_bar_layout(self):
        ptr = om.MQtUtil.findControl("flowLayout1")
        qt_layout = shiboken.wrapInstance(long(ptr), QtGui.QLayout)
        tool_bar_layout = qt_layout.children()[0].layout()
        self.tool_bar_layout = tool_bar_layout

    def add(self, qt_widget):
        self.tool_bar_layout.addWidget(qt_widget)

    def delete(self, widget):
        try:
            widget.deleteLater()
        except:
            self.logger.warning("%s does not exist.")
