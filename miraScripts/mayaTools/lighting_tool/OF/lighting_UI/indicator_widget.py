__author__ = 'heshuai'


from PySide import QtGui,QtCore
from get_parent_dir import get_parent_dir
import os


class ShapeWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ShapeWidget, self).__init__(parent)
        self.parent_dir = get_parent_dir()
        self.icon_path = os.path.join(self.parent_dir, 'icons', 'logo.png')

        pix = QtGui.QPixmap(self.icon_path, "0", QtCore.Qt.AvoidDither|QtCore.Qt.ThresholdDither|QtCore.Qt.ThresholdAlphaDither)
        self.resize(pix.size())
        self.setMask(pix.mask())
        self.dragPosition = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
        if event.button() == QtCore.Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos()-self.dragPosition)
            event.accept()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, QtGui.QPixmap(self.icon_path))
