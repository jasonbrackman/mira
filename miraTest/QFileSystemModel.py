# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore


class Main(QtGui.QTreeView):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.model = QtGui.QFileSystemModel()
        # print QtCore.QDir.currentPath()
        # index = self.model.setRootPath(QtCore.QDir.currentPath())
        root_path = r"D:\sct\assets\character\newbee\mdl"
        self.model.setRootPath(root_path)
        self.setModel(self.model)

        index = self.model.index(root_path)
        self.setRootIndex(index)

        self.resizeColumnToContents(1)

        selected_model = self.selectionModel()
        selected_model.selectionChanged.connect(self.do_test)

    def do_test(self, selected, deselected):
        indexes = selected.indexes()
        index = indexes[0]
        print self.model.filePath(index)


import sys
app = QtGui.QApplication(sys.argv)
m = Main()
m.show()
app.exec_()


