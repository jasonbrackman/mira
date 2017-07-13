#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'


from PySide.QtGui import *
from PySide.QtCore import *


class TaskFileList(QTreeView):
    def __init__(self, parent=None):
        super(TaskFileList, self).__init__(parent)

        self.__model = QFileSystemModel()

        self.setModel(self.__model)

        self.set_root(u'D:\SnowKidTest')

    def set_root(self, root=''):
        self.setRootIndex(self.__model.setRootPath(root))


class FileWidget(QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)

        '''init data'''

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

        self.__workList = TaskFileList()
        self.__publishList = TaskFileList()

        '''add layout'''
        main_layout.addLayout(file_layout)
        # file_layout.addLayout(file_work_layout)
        # file_layout.addLayout(file_publish_layout)

        '''add widget'''
        file_layout.addWidget(file_work_grp)
        file_layout.addWidget(file_publish_grp)
        file_work_layout.addWidget(self.__workList)
        file_publish_layout.addWidget(self.__publishList)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    tm = FileWidget()
    tm.show()
    app.exec_()

