#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'

from functools import partial
from PySide.QtGui import *
from PySide.QtCore import *
import os
import re


class TaskFileList(QTreeView):
    def __init__(self, parent=None):
        super(TaskFileList, self).__init__(parent)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__context_menu)

        self.__model = QFileSystemModel()
        self.__model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.AllEntries)
        self.__model.setNameFilterDisables(False)
        self.setModel(self.__model)

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        # self.set_root(u'W:/SnowKidTest/workarea/assets/Character/Jiegrandpa')
        # header = self.header()
        # header.setVisible(False)
        # # header.setClickable(False)  # 设置表头不可点击（默认点击后进行排序）
        # header.setStretchLastSection(True)  # 设置充满表宽度
        # # header.setResizeMode(QtGui.QHeaderView.Fixed)  # 设置拖拽
        # # header.setResizeMode(0, QtGui.QHeaderView.Fixed)
        # header.setFixedHeight(20)  # 设置表头高度

    def __context_menu(self, point):
        index = self.indexAt(point)
        if index.isValid():
            file_model = self.model()
            menu = QMenu(self)
            if not file_model.isDir(index):
                file_action = QAction(u'Open File..', self)
                file_action.triggered.connect(partial(self.__view_file, file_model.filePath(index)))
                menu.addAction(file_action)

            folder_action = QAction(u'Open Path..', self)

            path = file_model.filePath(index)
            if os.path.isfile(path):
                path = os.path.dirname(path)
            folder_action.triggered.connect(partial(self.__view_file, path))
            menu.addAction(folder_action)
            menu.exec_(self.mapToGlobal(point))

    @staticmethod
    def __view_file(file_info):
        if os.name == 'nt':
            try:
                os.startfile(file_info)
            except:
                pass

    def set_root(self, root=''):
        self.setRootIndex(self.__model.setRootPath(root))

    def set_filter(self, filters=[]):
        # self.__model.setFilterWildcard(ss)
        self.__model.setNameFilters(filters)
        self.__model.setNameFilterDisables(False)
        self.setModel(self.__model)


class FileView(QWidget):
    def __init__(self, parent=None):
        super(FileView, self).__init__(parent)

        '''create layout'''
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        '''create widget'''
        self.__filter_suffix_line = QLineEdit()
        self.__filter_suffix_line.setStyleSheet('QLineEdit {background-image: '
                                                'url(search.ico);background-repeat: no-repeat;'
                                                'background-position: right}')
        self.__filter_suffix_line.setValidator(QRegExpValidator(QRegExp('[a-zA-Z0-9,]+')))
        self.__filter_suffix_line.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        # self.__filter_suffix_line.setContentsMargins(100, 0, 0, 0)
        # self.__filter_suffix_line.setMaximumHeight(5)
        self.__filter_suffix_line.textEdited.connect(self.__change_filter)
        self.__filter_suffix_line.setPlaceholderText('Filter.. \"(*.*)\"')

        self.__fileView = TaskFileList()

        '''add widget'''
        main_layout.addWidget(self.__filter_suffix_line)
        main_layout.addWidget(self.__fileView)

    def __change_filter(self):
        filters = []
        for x in re.split(re.compile(r','), self.__filter_suffix_line.text()):
            filters.append('*.%s' % x)
        self.__fileView.set_filter(filters)

    def set_root(self, root=''):
        self.__fileView.set_root(root)

    #     self.__set_filter()
    #     # self.__file_list.set_filters(self.__name_filters)
    #
    # def __set_filter(self):
    #     file_list_model = self.model()
    #     if file_list_model is not None:
    #         file_list_model.setNameFilters(self.__name_filters)


class FileWidget(QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)

        '''create layout'''
        main_layout = QVBoxLayout(self)
        file_layout = QHBoxLayout()
        file_work_layout = QVBoxLayout()
        file_publish_layout = QVBoxLayout()

        '''create widget'''
        file_work_grp = QGroupBox('Workarea')
        file_work_grp.setLayout(file_work_layout)

        file_publish_grp = QGroupBox('Publish')
        file_publish_grp.setLayout(file_publish_layout)

        self.__workareaList = FileView(self)
        self.__publishList = FileView(self)

        '''add layout'''
        main_layout.addLayout(file_layout)
        # file_layout.addLayout(file_work_layout)
        # file_layout.addLayout(file_publish_layout)

        '''add widget'''
        file_layout.addWidget(file_work_grp)
        file_layout.addWidget(file_publish_grp)
        file_work_layout.addWidget(self.__workareaList)
        file_publish_layout.addWidget(self.__publishList)

    def set_workarea(self, root=''):
        self.__workareaList.set_root(root)

    def set_publish(self, root=''):
        self.__publishList.set_root(root)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    tm = FileWidget()
    tm.show()
    app.exec_()

