# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraLibs.pipeLibs.get_task_name import get_task_name
from miraFramework.task_common_form import CommonForm
from miraFramework.message_box import MessageWidget
from miraLibs.pyLibs import Path, join_path
from miraLibs.pipeLibs import pipeFile
from miraLibs.deadlineLibs import submit
from miraLibs.qtLibs import render_ui
import getpass


class TaskPublish(QDialog):
    def __init__(self, parent=None):
        super(TaskPublish, self).__init__(parent)
        self.setup_ui()
        self.set_style()
        self.set_signals()

    def setup_ui(self):
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Task Publish")
        self.resize(800, 600)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.common_widget = CommonForm()
        bottom_layout = QHBoxLayout()
        self.path_le = QLineEdit()
        self.path_btn = QToolButton()
        icon = QIcon()
        icon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon))
        self.path_btn.setIcon(icon)
        bottom_layout.addWidget(self.path_le)
        bottom_layout.addWidget(self.path_btn)

        btn_layout = QHBoxLayout()
        status_label = QLabel("Task Status: ")
        self.task_status_label = QLabel()
        self.task_status_check = QCheckBox("Change task status to Delivered")
        self.task_status_check.setChecked(True)
        self.publish_btn = QPushButton("Publish")
        self.publish_btn.setEnabled(False)
        btn_layout.addWidget(status_label)
        btn_layout.addWidget(self.task_status_label)
        btn_layout.addStretch()
        btn_layout.addWidget(self.task_status_check)
        btn_layout.addWidget(self.publish_btn)

        main_layout.addWidget(self.common_widget)
        main_layout.addLayout(bottom_layout)
        main_layout.addLayout(btn_layout)

    def set_style(self):
        qss_path = join_path.join_path2(os.path.dirname(__file__), "style.qss")
        self.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

    def set_signals(self):
        self.common_widget.fourth_widget.list_view.clicked.connect(self.show_path)
        self.path_btn.clicked.connect(self.open_dir)
        self.path_le.textChanged.connect(self.on_path_changed)
        self.publish_btn.clicked.connect(self.do_publish)

    @property
    def work_file(self):
        return self.path_le.text()

    @property
    def task_info(self):
        return self.common_widget.task_info

    def show_path(self):
        task_info = self.task_info
        if not task_info:
            self.path_le.setText("")
            self.task_status_label.setText("")
        else:
            # sg
            # work_file_path = self.task_info["sg_workfile"]
            # st
            status_color = task_info.get("status").get("color")
            status_name = task_info.get("status").get("name")
            self.task_status_label.setText("<font color=%s><b>%s</b></font>" % (status_color, status_name))
            json_data = task_info.get("json")
            if json_data and json_data. has_key("work_file_path"):
                self.path_le.setText(json_data.get("work_file_path"))
            else:
                self.path_le.setText("")

    def on_path_changed(self, work_file_path):
        if os.path.isfile(work_file_path):
            self.publish_btn.setEnabled(True)
        else:
            self.publish_btn.setEnabled(False)

    def open_dir(self):
        path = self.path_le.text()
        if path:
            p = Path.Path(path)
            dir_name = Path.Path(p.dirname())
            dir_name.startfile()

    def do_publish(self):
        if not self.work_file:
            return
        publish_script_path = join_path.join_path2(__file__, "..", "publish.py")
        obj = pipeFile.PathDetails.parse_path(self.work_file)
        task_name = get_task_name(obj)
        deadline_job_name = "publish_%s" % task_name
        change_status = self.task_status_check.isChecked()
        # work_file, change_task
        argv = "%s %s" % (self.work_file, change_status)
        submitter = getpass.getuser()
        tar_name = 'pipemanager'
        submit.submit_python_job(deadline_job_name, publish_script_path, argv, tar_name, submitter)
        mw = MessageWidget("Success", "%s submit done." % task_name, self)
        mw.show()


def main():
    render_ui.render(TaskPublish)


if __name__ == "__main__":
    main()
