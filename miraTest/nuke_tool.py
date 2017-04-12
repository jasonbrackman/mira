# -*- coding: utf-8 -*-
import sys
from PySide import QtGui, QtCore


class Panel(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Panel, self).__init__(parent)

        self.resize(400, 400)
        mouse_position = QtGui.QCursor().pos()
        self.center = QtCore.QPoint(self.width()/2, self.height()/2)
        self.move(mouse_position - self.center)
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose)

        self.selected_item = None
        self.mouse_destination = self.center
        self.layout = QtGui.QGridLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        for i in xrange(3):
            label = QtGui.QLabel(str(i))
            label.setFixedSize(100, 20)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("background: #FF0000")
            self.layout.addWidget(label, 0, i)
        self.setLayout(self.layout)

    def paintEvent(self, event):
        super(Panel, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        self.draw_line(painter)
        pixmap = QtGui.QPixmap("E:/nuke.png")
        painter.drawPixmap(QtCore.QPoint(self.width()/2-24, self.height()/2-24), pixmap)

    def draw_line(self, painter):
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        painter.setPen(pen)
        pen.setWidth(2)
        center = QtCore.QPoint(self.width()/2, self.height()/2)
        destionation = self.mouse_destination
        self.line = QtGui.QPolygon([center, center + QtCore.QPoint(1, 0), destionation, destionation+QtCore.QPoint(-1, 0)])
        painter.drawPolygon(self.line)

    def mouseMoveEvent(self, event):
        self.mouse_destination = event.pos()
        self.update()
        widgets = [self.layout.itemAt(i).widget() for i in xrange(self.layout.count())]
        for widget in widgets:
            if self.line.intersected(widget.geometry()):
                self.selected_item = widget
                widget.setStyleSheet("background: #00FF00")
            else:
                widget.setStyleSheet("background: #FF0000")


app = QtGui.QApplication(sys.argv)
pane = Panel()
pane.show()
sys.exit(app.exec_())
