# -*- coding: utf-8 -*-
import math
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *


class Waiting(QWidget):
    def __init__(self, parent=None):
        super(Waiting, self).__init__(parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))
        for i in range(12):
            if (self.counter / 11) % 12 == i:
                # painter.setBrush(QBrush(QColor(127 + (self.counter % 11)*16, 127, 127)))
                painter.setBrush(QBrush(QColor(255, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width() / 2 + 30 * math.cos(2 * math.pi * i / 12.0) - 10,
                self.height() / 2 + 30 * math.sin(2 * math.pi * i / 12.0) - 10,
                10, 10)

        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(5)
        self.counter = 0

    def timerEvent(self, event):
        self.counter += 1
        self.update()

    def quit(self):
        self.killTimer(self.timer)
        self.hide()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Waiting()
    w.show()
    app.exec_()
