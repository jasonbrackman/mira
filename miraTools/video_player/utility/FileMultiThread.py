# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class FileMultiThread(QThread):
    thread_finished = Signal()

    def __init__(self, cmd=None, parent=None):
        super(FileMultiThread, self).__init__(parent)
        self.cmd = cmd
        self.finished.connect(self.callback)

    def run(self):
        os.popen(self.cmd)

    def callback(self):
        self.thread_finished.emit()
