# -*- coding: utf-8 -*-
import sys
from PySide import QtGui, QtCore


class Panel(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Panel, self).__init__(parent)
        self.color = QtGui.QColor(255, 0, 0)
        self.origin = None
        self.destination = None

    def paintEvent(self, event):
        super(Panel, self).paintEvent(event)

        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush(self.color)
        painter.setBrush(brush)
        rect = QtCore.QRect(50, 50, 50, 50)
        painter.drawRect(rect)

        if not self.origin:
            return
        point1 = self.origin
        point2 = self.origin + QtCore.QPoint(10, 0)
        point3 = self.destination
        point4 = self.destination + QtCore.QPoint(-10, 0)

        poly = QtGui.QPolygon([point1, point2, point3, point4])
        painter.drawPolygon(poly)

        if poly.intersected():
            print "intersected"

    def mousePressEvent(self, event):
        self.origin = event.pos()

    def mouseMoveEvent(self, event):
        self.destination = event.pos()
        self.update()


app = QtGui.QApplication(sys.argv)
pane = Panel()
pane.show()
sys.exit(app.exec_())
