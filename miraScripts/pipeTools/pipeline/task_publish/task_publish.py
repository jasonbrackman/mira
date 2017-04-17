# -*- coding: utf-8 -*-
import os
from PySide import QtGui, QtCore
from get_task_name import get_task_name
from miraFramework.task_common_form import CommonForm
from miraLibs.pyLibs import Path, join_path
from miraLibs.pipeLibs import pipeFile
from miraLibs.deadlineLibs import submit


class TaskPublish(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TaskPublish, self).__init__(parent)
        self.setup_ui()
        self.set_style()
        self.set_signals()

    def setup_ui(self):
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Task Publish")
        self.resize(700, 400)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.common_widget = CommonForm()
        bottom_layout = QtGui.QHBoxLayout()
        self.path_le = QtGui.QLineEdit()
        self.path_btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.path_btn.setIcon(icon)
        bottom_layout.addWidget(self.path_le)
        bottom_layout.addWidget(self.path_btn)

        btn_layout = QtGui.QHBoxLayout()
        self.task_status_check = QtGui.QCheckBox("Change task status to final")
        self.task_status_check.setChecked(True)
        self.publish_btn = QtGui.QPushButton("Publish")
        self.publish_btn.setEnabled(False)
        btn_layout.addStretch()
        btn_layout.addWidget(self.task_status_check)
        btn_layout.addWidget(self.publish_btn)

        main_layout.addWidget(self.common_widget)
        main_layout.addLayout(bottom_layout)
        main_layout.addLayout(btn_layout)

    def set_style(self):
        qss_path = join_path.join_path2(os.path.dirname(__file__), "style.qss")
        self.setStyle(QtGui.QStyleFactory.create('plastique'))
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
        if not self.task_info:
            self.path_le.setText("")
        else:
            work_file_path = self.task_info["sg_workfile"]
            if work_file_path:
                self.path_le.setText(work_file_path)
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
        publish_script_path = join_path.join_path2("__file__", "..", "publish.py")
        obj = pipeFile.PathDetails.parse_path(self.work_file)
        task_name = get_task_name(obj)
        deadline_job_name = "%s_%s" % (obj.project, task_name)
        change_status = self.task_status_check.isChecked()
        # work_file, change_task
        argv = "%s %s" % (self.work_file, change_status)
        submitter = u'heshuai'
        tar_name = u'heshuai'
        submit.submit_python_job(deadline_job_name, publish_script_path, argv, submitter, tar_name)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    tm = TaskPublish()
    tm.show()
    app.exec_()
