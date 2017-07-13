#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'

from PySide.QtGui import *
from PySide.QtCore import *


class TaskTreeModel(QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(TaskTreeModel, self).__init__(parent)
        self.__rootNode = root

    def headerData(self, section, orientation, role):
        pass

    def rowCount(self, parent):
        if not parent.isValid():
            parent_node = self.__rootNode
        else:
            parent_node = parent.internalPointer()

        if parent_node:
            return parent_node.count()
        else:
            return 0

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.SizeHintRole:
            return QSize(50, 50)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return node.name
        # # if role == QtCore.Qt.ToolTipRole:
        # #     return 'Tags: ' + ' '.join(self.__information_list[row].tags) + '\nMaterial tags: ' + \
        # #            ' '.join(self.__information_list[row].material_tags)
        # # if role == QtCore.Qt.TextAlignmentRole:
        # #     return QtCore.Qt.AlignCenter
        # #     # return self.__information_list[row].abc
        # if role == QtCore.Qt.DecorationRole or role == QtCore.Qt.EditRole:
        #     pixmap = QtGui.QPixmap(48, 48)
        #     pixmap.load(node.thumbnail())
        #     icon = QtGui.QIcon(pixmap)
        #     return icon

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    # def setData(self, index, value, role=Qt.EditRole):
    #     if role == Qt.EditRole and index.isValid():
    #         if not not len(value):
    #             node = index.internalPointer()
    #             node.set_name(value.capitalize())
    #             self.dataChanged.emit(index, index)
    #             return True
    #         return False
    #     return False

    def parent(self, index):
        # print index.row()
        # print index.column()

        node = index.internalPointer()
        parent_node = node.parent

        if parent_node == self.__rootNode:
            return QModelIndex()

        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        if not parent.isValid():
            parent_node = self.__rootNode
        else:
            parent_node = parent.internalPointer()

        child_item = parent_node.child(row)

        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()


class TaskTreeView(QTreeView):
    def __init__(self, parent=None):
        super(TaskTreeView, self).__init__(parent)

        self.assetModel = TaskTreeModel(None)
        self.shotModel = TaskTreeModel(None)
        self.setModel(self.assetModel)

        '''init data'''
        self.__project = ''
        # self.__st =

    def set_project(self, project=''):
        self.__project = project


class TaskWidget(QWidget):
    def __init__(self, parent=None):
        super(TaskWidget, self).__init__(parent)

        '''init data'''
        self.__parent = parent
        self.__project = ''
        self.__assetData = None

        '''create layout'''
        main_layout = QVBoxLayout(self)
        tool_layout = QVBoxLayout()
        radio_layout = QHBoxLayout()
        tree_layout = QHBoxLayout()

        '''create widget'''
        task_grp = QGroupBox("Task")
        task_grp.setLayout(tool_layout)

        self.mode_bg = QButtonGroup()

        asset_radio = QRadioButton('Asset')
        asset_radio.setFocusPolicy(Qt.NoFocus)
        asset_shot = QRadioButton('Shot')
        asset_shot.setFocusPolicy(Qt.NoFocus)

        self.mode_bg.addButton(asset_radio, 1)
        self.mode_bg.addButton(asset_shot, 2)

        self.treeView = TaskTreeView()

        '''add widget'''
        main_layout.addWidget(task_grp)
        radio_layout.addWidget(asset_radio)
        radio_layout.addWidget(asset_shot)
        tree_layout.addWidget(self.treeView)

        '''add layout'''
        tool_layout.addLayout(radio_layout)
        tool_layout.addLayout(tree_layout)

        '''connect'''
        self.mode_bg.buttonClicked.connect(self.__set_view)

    def set_data(self, data):
        print 'set_data'
        self.__assetData = data

    def set_project(self, project):
        print 'set_project'
        self.__project = project
        self.treeView.set_project(project)
        asset_root = self.__assetData.asset_root[project]
        shot_root = self.__assetData
        self.treeView.assetModel = TaskTreeModel(asset_root)
        self.treeView.shotModel = TaskTreeModel(shot_root)
        self.__set_view()

    def __set_view(self):
        print 'set_view'
        mode = self.mode_bg.checkedId()
        if mode == 1:
            self.treeView.setModel(self.treeView.assetModel)
        elif mode == 2:
            self.treeView.setModel(self.treeView.shotModel)
        else:
            pass
        self.__parent.change_task()

if __name__ == "__main__":
    pass


