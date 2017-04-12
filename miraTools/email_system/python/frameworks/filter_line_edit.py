# -*- coding: utf-8 -*-
import os
from PySide import QtGui, QtCore
from ..libs import get_icon_dir


def get_icon_file():
    icon_dir = get_icon_dir.get_icon_dir()
    icon_file = os.path.join(icon_dir, "search.png").replace("\\", "/")
    return icon_file


class FilterLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(FilterLineEdit, self).__init__(parent)
        self.icon_file = get_icon_file()
        self.button = QtGui.QToolButton(self)
        self.button.setEnabled(False)
        self.button.setIcon(QtGui.QIcon(self.icon_file))
        self.button.setStyleSheet("QToolButton{border: 0px; padding: 0px; background:transparent}"\
                                  "QToolButton::hover{background:transparent}")
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.editingFinished)

        frame_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        button_size = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (button_size.width() + frame_width + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), button_size.width() + frame_width*2 + 2),
                            max(self.minimumSizeHint().height(), button_size.height() + frame_width*2 + 2))

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        frame_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frame_width - button_size.width(),
                         (self.rect().bottom() - button_size.height() + 1)/2)
        super(FilterLineEdit, self).resizeEvent(event)
