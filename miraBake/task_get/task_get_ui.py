# -*- coding: utf-8 -*-
import os

from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *

from miraFramework.Filter import Filter
from miraFramework.combo import ProjectCombo
from miraFramework.refresh_btn import RefreshButton
from miraLibs.dccLibs import FileOpener
from miraLibs.dccLibs import get_engine
from miraLibs.pyLibs import start_file


class FileTreeView(QTreeView):
    def __init__(self, name=None, parent=None):
        super(FileTreeView, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.name = name
        self.expandAll()
        self.header().setVisible(False)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setSortingEnabled(True)
        self.menu = QMenu(self)
        self.open_action = QAction("Open", self)
        self.copy_to_local_action = QAction("Receive The Task", self)
        self.show_in_filesystem_action = QAction("Show in File System", self)
        self.set_signals()

    def set_signals(self):
        self.open_action.triggered.connect(self.do_open)
        self.show_in_filesystem_action.triggered.connect(self.show_in_filesystem)

    def contextMenuEvent(self, event):
        self.menu.clear()
        self.menu.addAction(self.open_action)
        self.menu.addAction(self.show_in_filesystem_action)
        if self.name == "work":
            self.menu.addAction(self.copy_to_local_action)
        self.menu.exec_(QCursor.pos())
        event.accept()

    def get_filter(self):
        app = get_engine.get_engine()
        filter_list = []
        if app == "maya":
            filter_list = ["*.ma", "*.mb"]
        elif app == "python":
            filter_list = []
        elif app == "nuke":
            filter_list = ["*.nk"]
        elif app == "houdini":
            filter_list = ["*.hip"]
        return filter_list

    def set_dir(self, file_dir):
        if os.path.isdir(file_dir):
            self.model = QFileSystemModel()
            filter_list = self.get_filter()
            # self.model.setFilter(QDir.Files | QDir.NoDotAndDotDot)
            self.model.setNameFilters(filter_list)
            self.model.setNameFilterDisables(False)
            self.setModel(self.model)
            root_index = self.model.setRootPath(file_dir)
            self.setRootIndex(root_index)
            self.hideColumn(1)
            self.hideColumn(2)
            self.hideColumn(3)
        else:
            self.model = QStandardItemModel()
            self.setModel(self.model)

    def get_selected(self):
        indexes = self.selectedIndexes()
        if not indexes:
            return
        file_paths = [self.model.filePath(index) for index in indexes if index.column() == 0]
        file_paths = list(set(file_paths))
        return file_paths

    def do_open(self):
        file_paths = self.get_selected()
        if not file_paths:
            return
        file_path = file_paths[0]
        fo = FileOpener.FileOpener(file_path)
        fo.run()

    def show_in_filesystem(self):
        file_paths = self.get_selected()
        if not file_paths:
            return
        file_path = file_paths[0]
        if os.path.isfile(file_path):
            dir_name = os.path.dirname(file_path)
        elif os.path.isdir(file_path):
            dir_name = file_path
        start_file.start_file(dir_name)

    def clear(self):
        model = QStandardItemModel()
        self.setModel(model)


class TaskGetUI(QDialog):
    def __init__(self, parent=None):
        super(TaskGetUI, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Task get")
        self.setObjectName("Task get")
        self.resize(750, 630)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        project_layout = QHBoxLayout()
        project_label = QLabel("Project")
        project_label.setFixedWidth(50)
        self.project_cbox = ProjectCombo()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        main_splitter = QSplitter(Qt.Horizontal, self)

        task_widget = QTabWidget()
        my_task_widget = QWidget()
        task_widget.addTab(my_task_widget, "My Tasks")
        my_task_layout = QVBoxLayout(my_task_widget)
        self.filter_le = Filter()
        mid_layout = QHBoxLayout()
        self.final_checkbox = QCheckBox("Delivered")
        self.final_checkbox.setChecked(False)
        self.refresh_btn = RefreshButton()
        mid_layout.addWidget(self.final_checkbox)
        mid_layout.addStretch()
        mid_layout.addWidget(self.refresh_btn)
        self.task_view = QTreeView()
        my_task_layout.addWidget(self.filter_le)
        my_task_layout.addLayout(mid_layout)
        my_task_layout.addWidget(self.task_view)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)

        detail_widget = QWidget()
        layout = QVBoxLayout(detail_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        detail_group = QGroupBox()
        layout.addWidget(detail_group)
        detail_layout = QGridLayout(detail_group)
        status_label = QLabel()
        status_label.setText("<font size=3 color=#DDD>Stauts:</font>")
        self.status_label = QLabel()
        due_label = QLabel()
        due_label.setText("<font size=3 color=#DDD>Due Date:</font>")
        self.due_label = QLabel()
        detail_layout.addWidget(status_label, 0, 0, 1, 1)
        detail_layout.addWidget(self.status_label, 0, 1, 1, 4)
        detail_layout.addWidget(due_label, 1, 0, 1, 1)
        detail_layout.addWidget(self.due_label, 1, 1, 1, 4)
        detail_layout.setVerticalSpacing(11)

        init_layout = QHBoxLayout()
        init_layout.setContentsMargins(0, 0, 0, 0)
        self.init_btn = QPushButton("+ Initialize Task")
        self.init_btn.setStyleSheet("color: #00b4ff; font-size: 10pt; font-weight: bold; ")
        init_layout.addStretch()
        init_layout.addWidget(self.init_btn)

        self.file_widget = QTabWidget()
        self.local_file_widget = FileTreeView("local")
        self.work_file_widget = FileTreeView("work")
        self.publish_file_widget = FileTreeView("publish")
        self.file_widget.addTab(self.local_file_widget, "Local")
        self.file_widget.addTab(self.work_file_widget, "Working")
        self.file_widget.addTab(self.publish_file_widget, "Publishes")

        info_layout.addWidget(detail_widget)
        info_layout.addLayout(init_layout)
        info_layout.addWidget(self.file_widget)

        main_splitter.addWidget(task_widget)
        main_splitter.addWidget(info_widget)

        main_splitter.setSizes([self.width()*0.45, self.width()*0.55])
        main_splitter.setStretchFactor(1, 1)

        main_layout.addLayout(project_layout)
        main_layout.addWidget(main_splitter)


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(TaskGetUI)



