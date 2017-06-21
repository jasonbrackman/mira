# -*- coding: utf-8 -*-
import sys
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class Panel(QWidget):
    def __init__(self, parent=None):
        super(Panel, self).__init__(parent)
        self.resize(500, 500)
        self.origin = None
        self.destination = None
        self.lines = list()

    def paintEvent(self, event):
        super(Panel, self).paintEvent(event)
        if self.origin is None:
            return
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 255))
        painter.setPen(pen)
        for line in self.lines:
            painter.drawLine(line)

    def mousePressEvent(self, event):
        self.origin = event.pos()

    def mouseMoveEvent(self, event):
        self.destination = event.pos()
        line = QLine(self.origin, self.destination)
        self.lines.append(line)
        self.origin = self.destination
        self.update()


app = QApplication(sys.argv)
pane = Panel()
pane.show()
sys.exit(app.exec_())
