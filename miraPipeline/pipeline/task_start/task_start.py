# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, "Z:/mira")
from PySide import QtGui, QtCore
from miraLibs.pipeLibs.get_task_name import get_task_name
from miraFramework.task_common_form import CommonForm
from miraLibs.pyLibs import Path, join_path
from miraLibs.pipeLibs import pipeFile
from miraLibs.deadlineLibs import submit


class TaskStart(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TaskStart, self).__init__(parent)
        self.setup_ui()
        self.set_style()
        self.set_signals()

    def setup_ui(self):
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Task Start")
        self.resize(800, 600)
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
        self.start_btn = QtGui.QPushButton("Start")
        btn_layout.addStretch()
        btn_layout.addWidget(self.start_btn)

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
        self.start_btn.clicked.connect(self.do_start)

    @property
    def work_file(self):
        return self.path_le.text()

    @property
    def task_info(self):
        return self.common_widget.task_info

    def show_path(self):
        project = self.common_widget.project
        engine = self.common_widget.engine
        entity_type = self.common_widget.entity_type
        asset_type_or_sequence = self.common_widget.asset_type_or_sequence
        asset_or_shot = self.common_widget.asset_or_shot
        step = self.common_widget.step
        task = self.common_widget.task
        if not all((asset_type_or_sequence, asset_or_shot, step, task)):
            return
        if entity_type == "Asset":

            file_path = pipeFile.get_asset_task_work_file(project, asset_type_or_sequence, asset_or_shot, step, task,
                                                          "000", engine)
        else:
            file_path = pipeFile.get_shot_task_work_file(project, asset_type_or_sequence, asset_or_shot, step, task,
                                                         "000", engine)
        self.path_le.setText(file_path)

    def open_dir(self):
        path = self.path_le.text()
        if path:
            p = Path.Path(path)
            dir_name = Path.Path(p.dirname())
            dir_name.startfile()

    def do_start(self):
        if not self.work_file:
            return
        start_script_path = join_path.join_path2("__file__", "..", "start.py")
        obj = pipeFile.PathDetails.parse_path(self.work_file)
        task_name = get_task_name(obj)
        deadline_job_name = "start_%s" % task_name
        # work_file, change_task
        argv = self.work_file
        submitter = u'heshuai'
        tar_name = u'heshuai'
        submit.submit_python_job(deadline_job_name, start_script_path, argv, submitter, tar_name)


def main():
    app = QtGui.QApplication(sys.argv)
    tm = TaskStart()
    tm.show()
    app.exec_()


if __name__ == "__main__":
    main()
