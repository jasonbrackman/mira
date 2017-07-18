#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'


# from Qt.QtWidgets import *
# from Qt.QtCore import *
# from Qt.QtGui import *

from PySide.QtGui import *
from PySide.QtCore import *

# import maya.utils as utils
import sys
import os
import task_tree_ui
import task_file_list_ui
import task_object

reload(task_tree_ui)
reload(task_file_list_ui)
reload(task_object)


class CollectThread(QThread):
    signal = Signal(task_object.TaskObject)

    def __init__(self, func, parent=None):
        super(CollectThread, self).__init__(parent)
        self.__function = func

    def run(self):
        # self.signal.emit(utils.executeInMainThreadWithResult(self.__function))
        self.signal.emit(self.__function)


class TaskManager(QDialog):
    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle('Task Manager')
        self.setMinimumSize(1600, 600)
        self.setStyleSheet("font-family: DesiredFont;")
        # self.setChildrenCollapsible(False)
        # self.setFrameShape(QFrame.StyledPanel)

        '''init data'''
        self.__show_thread = CollectThread(task_object.TaskObject())
        self.__taskObject = None
        self.__workarea_path = ''
        self.__publish_path = ''

        '''create layout'''
        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        tool_layout = QHBoxLayout()
        sub_layout = QHBoxLayout()
        # sub_layout.setContentsMargins(0,0,0,0)

        '''create widget'''
        project_label = QLabel("Project")
        project_label.setFixedWidth(50)

        self.__project_combo = QComboBox()

        main_splitter = QSplitter(Qt.Horizontal, self)
        main_splitter.setStretchFactor(1, 1)
        main_splitter.setStyleSheet("QSplitter::handle { image: none; }")
        main_splitter.setContentsMargins(5, 5, 5, 5)
        main_splitter.setFrameStyle(QFrame.Panel | QFrame.Raised)

        self.__task_tree = task_tree_ui.TaskWidget(self)

        self.__task_file = task_file_list_ui.FileWidget(self)

        '''add layout'''
        main_layout.addLayout(tool_layout)
        main_layout.addLayout(sub_layout)

        # main_splitter.setLayout(sub_layout)

        '''add widget'''
        tool_layout.addWidget(project_label)
        tool_layout.addWidget(self.__project_combo)

        main_splitter.addWidget(self.__task_tree)
        main_splitter.addWidget(self.__task_file)
        main_splitter.setSizes([self.width() * 0.2, self.width() * 0.8])

        sub_layout.addWidget(main_splitter)

        '''connect signal'''
        self.__project_combo.currentIndexChanged.connect(self.__set_project)
        self.__show_thread.signal.connect(self.__collect)
        self.__show_thread.start()

    def __collect(self, data):
        if not data:
            return

        self.__taskObject = data
        self.__task_tree.set_data(self.__taskObject)
        self.__project_combo.addItems(self.__taskObject.projects)
        self.__project_combo.setCurrentIndex(self.__project_combo.findText(self.__taskObject.current_project))

        self.__task_tree.treeView.clicked.connect(self.__path_change)

    def __set_project(self):
        self.__task_tree.set_project(self.__project_combo.currentText())
        # print self.__task_tree.mode_bg.checkedId()

    def change_task(self):
        print 'change_task', self

    def __path_change(self):
        selection = self.__task_tree.treeView.selectionModel()
        index = selection.currentIndex()
        node = selection.model().mapToSource(index).internalPointer()

        # print node.name

        if self.__workarea_path != node.workarea:
            self.__workarea_path = node.workarea
            if os.path.isdir(self.__workarea_path):
                self.__task_file.set_workarea(self.__workarea_path)

        if self.__publish_path != node.publish:
            self.__publish_path = node.publish
            if os.path.isdir(self.__publish_path):
                self.__task_file.set_publish(self.__publish_path)


def main():
    # from miraLibs.qtLibs import render_ui
    # render_ui.render(Task_Manager)
    app = QApplication(sys.argv)
    tm = TaskManager()
    tm.show()
    app.exec_()

if __name__ == "__main__":
    main()

