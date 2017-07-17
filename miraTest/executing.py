import time
import math, sys
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *


class RunThread(QThread):
    def __init__(self, parent=None):
        super(RunThread, self).__init__(parent)

    def run(self):
        time.sleep(2)


class Overlay(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
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
                   painter.setBrush(QBrush(QColor(127 + (self.counter % 11)*16, 127, 127)))
                   # painter.setBrush(QBrush(QColor(255, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width()/2 + 30 * math.cos(2 * math.pi * i / 12.0) - 10,
                self.height()/2 + 30 * math.sin(2 * math.pi * i / 12.0) - 10,
                10, 10)

        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(5)
        self.counter = 0

    def timerEvent(self, event):
        self.counter += 1
        self.update()
        # if self.counter == 60:
        #     self.killTimer(self.timer)
        #     self.hide()


class MainWindow(QMainWindow):

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)

        widget = QWidget(self)
        self.editor = QTextEdit()
        # self.editor.setPlainText("0123456789"*100)
        layout = QGridLayout(widget)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        button = QPushButton("Wait")
        layout.addWidget(button, 1, 1, 1, 1)

        self.setCentralWidget(widget)
        self.overlay = Overlay(self.centralWidget())
        self.overlay.hide()
        button.clicked.connect(self.waiting)

        self.threads = list()

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

    def waiting(self):
        self.overlay.show()
        # QCoreApplication.processEvents()
        t = RunThread()
        t.finished.connect(self.stop)
        self.threads.append(t)
        t.start()

    def stop(self):
        self.overlay.killTimer(self.overlay.timer)
        self.overlay.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
