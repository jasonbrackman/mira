# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class RealBaseCheck(object):
    def __init__(self, parent):
        self.check_result = "fail"
        self.info = None
        self.error_list = []

    def fail_check(self, value):
        self.check_result = "fail"
        self.info = value

    def pass_check(self, value):
        self.check_result = "pass"
        self.info = value

    def warning_check(self, value):
        self.check_result = "warning"
        self.info = value

    def ignore_check(self, value):
        self.check_result = "ignore"
        self.info = value

    def run(self):
        pass


class CheckProgress(QProgressDialog):
    def __init__(self, parent=None):
        super(CheckProgress, self).__init__(parent)
        self.setRange(1, 100)
        self.setModal(True)


class BaseCheck(RealBaseCheck):
    def __init__(self, parent=None):
        super(BaseCheck, self).__init__(parent)
        self.progress_dialog = CheckProgress()
        self.progress_dialog.setLabelText("Checking...Please wait.")

    def set_window_title(self, title):
        self.progress_dialog.setWindowTitle(title)

    def show(self):
        self.progress_dialog.setValue(30)
        self.progress_dialog.show()
        app = QApplication.instance()
        app.processEvents()

    def close(self):
        self.progress_dialog.close()
