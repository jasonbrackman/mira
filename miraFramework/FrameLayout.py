# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore


class FrameLayout(QtGui.QGridLayout):
    def __init__(self, button_text=None, collapse_status=None, parent=None):
        super(FrameLayout, self).__init__(parent)
        self.button_text = button_text
        self.collapse_status = collapse_status
        self.parent = parent

        self.setSpacing(0)

        self.tool_btn = QtGui.QToolButton()
        self.tool_btn.setFixedWidth(parent.width())
        self.tool_btn.setText(self.button_text)
        self.tool_btn.setIconSize(QtCore.QSize(6, 6))
        self.tool_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.tool_btn.setStyleSheet("QToolButton {background-color: #666666}")

        self.frame = QtGui.QFrame()
        self.frame.setFixedWidth(parent.width())
        self.frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Plain)

        self.addWidget(self.tool_btn, 0, 0)
        self.addWidget(self.frame, 1, 0)
        self.init_settings()
        self.set_signals()

    def init_settings(self):
        if self.collapse_status:
            self.tool_btn.setArrowType(QtCore.Qt.RightArrow)
            self.frame.setHidden(True)
        else:
            self.tool_btn.setArrowType(QtCore.Qt.DownArrow)
            self.frame.setHidden(False)

    def set_signals(self):
        self.tool_btn.clicked.connect(self.change_collapse)

    def change_collapse(self):
        self.collapse_status = not self.collapse_status
        self.init_settings()


if __name__ == "__main__":
    pass
