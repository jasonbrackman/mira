# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtGui import *

REFRESH_ICON = os.path.abspath(os.path.join(__file__, "..", "refresh.png")).replace("\\", "/")
HOVER_ICON = os.path.abspath(os.path.join(__file__, "..", "hover.png")).replace("\\", "/")


class RefreshButton(QToolButton):
    def __init__(self, parent=None):
        super(RefreshButton, self).__init__(parent)
        self.setIcon(QIcon(REFRESH_ICON))
        # style_sheet = "QToolButton{background: transparent;}QToolButton:hover{image: url(%s);}" % HOVER_ICON
        style_sheet = "QToolButton{background: transparent;}QToolButton:hover{background: #17a9e7;}"
        self.setStyleSheet(style_sheet)


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(RefreshButton)
