# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *


class TaskCellWidget(QWidget):
    def __init__(self, parent=None):
        super(TaskCellWidget, self).__init__(parent)
        main_layout = QHBoxLayout(self)
        self.pic_label = QLabel()
        info_layout = QVBoxLayout()
        self.entity_label = QLabel()
        self.step_task_label = QLabel()
        self.status_label = QLabel()
        self.date_label = QLabel()
        self.entity_label.setStyleSheet("background: transparent")
        self.step_task_label.setStyleSheet("background: transparent")
        self.status_label.setStyleSheet("background: transparent")
        self.date_label.setStyleSheet("background: transparent")
        info_layout.addWidget(self.entity_label)
        info_layout.addWidget(self.step_task_label)
        info_layout.addWidget(self.status_label)
        info_layout.addWidget(self.date_label)
        info_layout.setAlignment(Qt.AlignVCenter)
        # info_layout.setSpacing(0)
        main_layout.addWidget(self.pic_label)
        main_layout.addLayout(info_layout)
        # main_layout.setSpacing(10)
        main_layout.setStretchFactor(self.pic_label, 3)
        main_layout.setStretchFactor(info_layout, 3)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

    def set_picture(self, pix_map):
        self.pic_label.setPixmap(pix_map)

    def set_entity(self, entity_type, entity_name):
        self.entity_label.setText("<font size=4><b>%s - %s</b></font>" % (entity_type, entity_name))

    def set_step_task(self, step, task):
        self.step_task_label.setText("<font size=3></b>%s - %s</b></font>" % (step, task))

    def set_status(self, status_name, status_color):
        self.status_label.setText("<font size=3 color=%s><b>%s</b></font>" % (status_color, status_name))

    def set_date(self, start_date, due_date):
        self.date_label.setText("<font size=3>%s - %s" % (start_date, due_date))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    td = TaskCellWidget()
    td.set_picture("D:/pictures/CG/env.png")
    td.set_entity("Prop", "SnowKidTest")
    td.set_step_task("MidMdl", "MidMdl")
    td.set_status("Ready to start", "#ff9c00")
    td.set_date("2017-06-01", "2017-08-01")
    td.show()
    app.exec_()




