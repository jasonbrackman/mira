# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraFramework.Filter import ButtonLineEdit
from miraLibs.osLibs import FileOpener
from miraLibs.pyLibs import start_file
from miraLibs.osLibs import get_engine


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
        self.copy_to_local_action = QAction("Copy To Local", self)
        self.show_in_filesystem_action = QAction("Show In File System", self)
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
        self.resize(900, 700)
        self.setWindowTitle("Task get")
        self.setObjectName("Task get")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        project_layout = QHBoxLayout()
        project_label = QLabel("Project")
        project_label.setFixedWidth(50)
        self.project_cbox = QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        main_splitter = QSplitter(Qt.Horizontal)

        task_widget = QTabWidget()
        my_task_widget = QWidget()
        task_widget.addTab(my_task_widget, "My Tasks")
        my_task_layout = QVBoxLayout(my_task_widget)
        self.filter_le = ButtonLineEdit()
        self.final_checkbox = QCheckBox("Complete")
        self.final_checkbox.setChecked(False)
        self.task_view = QTreeView()
        my_task_layout.addWidget(self.filter_le)
        my_task_layout.addWidget(self.final_checkbox)
        my_task_layout.addWidget(self.task_view)

        self.file_widget = QTabWidget()
        self.local_file_widget = FileTreeView("local")
        self.work_file_widget = FileTreeView("work")
        self.publish_file_widget = FileTreeView("publish")
        self.file_widget.addTab(self.local_file_widget, "Local")
        self.file_widget.addTab(self.work_file_widget, "Working")
        self.file_widget.addTab(self.publish_file_widget, "Publishes")

        main_splitter.addWidget(task_widget)
        main_splitter.addWidget(self.file_widget)

        btn_layout = QHBoxLayout()
        self.open_btn = QPushButton("Open")
        btn_layout.addStretch()
        btn_layout.addWidget(self.open_btn)

        main_splitter.setSizes([self.width()*0.4, self.width()*0.6])

        main_layout.addLayout(project_layout)
        main_layout.addWidget(main_splitter)
        # main_layout.addLayout(btn_layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    tg = TaskGetUI()
    tg.show()
    app.exec_()



