# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from miraFramework.Filter import ButtonLineEdit


class TaskWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TaskWidget, self).__init__(parent)
        task_layout = QtGui.QVBoxLayout(self)
        self.filter_le = ButtonLineEdit()
        self.tree_view = QtGui.QTreeView()
        task_layout.addWidget(self.filter_le)
        task_layout.addWidget(self.tree_view)


class TaskPublish(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TaskPublish, self).__init__(parent)

        main_layout = QtGui.QHBoxLayout(self)
        main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        task_widget = QtGui.QTabWidget()
        self.asset_task_widget = TaskWidget()
        self.shot_task_widget = TaskWidget()

        task_widget.addTab(self.asset_task_widget, "Assets")
        task_widget.addTab(self.shot_task_widget, "Shots")

        opt_widget = QtGui.QWidget()


