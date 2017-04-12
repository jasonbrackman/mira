# -*- coding: utf-8 -*-
import os
from PySide import QtCore


class FileMultiThread(QtCore.QThread):
    thread_finished = QtCore.Signal()

    def __init__(self, cmd=None, parent=None):
        super(FileMultiThread, self).__init__(parent)
        self.cmd = cmd
        self.finished.connect(self.callback)

    def run(self):
        os.popen(self.cmd)

    def callback(self):
        self.thread_finished.emit()
