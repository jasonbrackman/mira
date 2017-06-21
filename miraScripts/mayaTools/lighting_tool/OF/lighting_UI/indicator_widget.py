__author__ = 'heshuai'


from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from get_parent_dir import get_parent_dir
import os


class ShapeWidget(QWidget):
    def __init__(self, parent=None):
        super(ShapeWidget, self).__init__(parent)
        self.parent_dir = get_parent_dir()
        self.icon_path = os.path.join(self.parent_dir, 'icons', 'logo.png')

        pix = QPixmap(self.icon_path, "0", Qt.AvoidDither|Qt.ThresholdDither|Qt.ThresholdAlphaDither)
        self.resize(pix.size())
        self.setMask(pix.mask())
        self.dragPosition = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
        if event.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos()-self.dragPosition)
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, QPixmap(self.icon_path))
