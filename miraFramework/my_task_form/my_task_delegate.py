# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from Qt.QtWebKit import *


class TaskCellWidget(QWidget):
    def __init__(self, parent=None):
        super(TaskCellWidget, self).__init__(parent)
        self.resize(380, 50)
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(30)
        self.web_view = QWebView()
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignTop)
        info_layout.setSpacing(10)
        self.entity_label = QLabel()
        self.step_task_label = QLabel()
        self.status_label = QLabel()
        self.date_label = QLabel()
        info_layout.addWidget(self.entity_label)
        info_layout.addWidget(self.step_task_label)
        info_layout.addWidget(self.status_label)
        info_layout.addWidget(self.date_label)
        main_layout.addWidget(self.web_view)
        main_layout.addLayout(info_layout)
        main_layout.setStretchFactor(self.web_view, 3)
        main_layout.setStretchFactor(info_layout, 3)

    def set_picture(self, picture_path):
        self.web_view.setHtml("<image src=%s>" % picture_path)
        self.web_view.setZoomFactor(0.7)

    def set_entity(self, entity_name):
        self.entity_label.setText("<font size=5><b>%s</b></font>" % entity_name)

    def set_step_task(self, step, task):
        self.step_task_label.setText("<font color=#ffffff>%s - %s</font>" % (step, task))

    def set_status(self, status_name, status_color):
        self.status_label.setText("<font size=4 color=%s><b>%s</b></font>" % (status_color, status_name))

    def set_date(self, start_date, due_date):
        self.date_label.setText("<font size=3>%s - %s" % (start_date, due_date))


if __name__ == "__main__":
    import sys
    # app = QApplication(sys.argv)
    td = TaskCellWidget()
    td.set_picture("http://192.168.0.220/strack/Uploads/TaskThumb/d58be76e_1497945424/task_1cb79ca51501233123_max.jpg")
    td.set_entity("SnowKidTest")
    td.set_step_task("MidMdl", "MidMdl")
    td.set_status("Ready to start", "#ff9c00")
    td.set_date("2017-06-01", "2017-08-01")
    td.show()
    # app.exec_()




