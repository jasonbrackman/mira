# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtGui, QtCore


class ThumbListWidget(QtGui.QListWidget):
    def __init__(self,  parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

        self.setIconSize(QtCore.QSize(150, 150))
        self.setViewMode(QtGui.QListView.IconMode)
        self.setResizeMode(QtGui.QListView.Adjust)
        self.setFlow(QtGui.QListView.LeftToRight)
        self.setSortingEnabled(True)
        # self.setMovement(QtGui.QListView.Static)
        self.setWrapping(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ThumbListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(ThumbListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.setDropAction(QtCore.Qt.CopyAction)
            super(ThumbListWidget, self).dropEvent(event)


class TestDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)
        main_layout = QtGui.QVBoxLayout(self)
        self.asset_list_widget = ThumbListWidget()
        self.asset_list_widget.setAcceptDrops(False)
        self.include_list_widget = ThumbListWidget()
        main_layout.addWidget(self.asset_list_widget)
        main_layout.addWidget(self.include_list_widget)
        self.init()

    def init(self):
        for i in ["Render26", "Render27", "Render36", "Render37B"]:
            item = QtGui.QListWidgetItem(i)
            icon_path = os.path.normpath(os.path.join("D:/pictures", i))
            item.setIcon(QtGui.QIcon(icon_path))
            self.asset_list_widget.addItem(item)


app = QtGui.QApplication(sys.argv)
td = TestDialog()
td.show()
app.exec_()


if __name__ == "__main__":
    pass
