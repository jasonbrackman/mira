# -*- coding: utf-8 -*-
import os
import sys
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class ThumbListWidget(QListWidget):
    def __init__(self,  parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QSize(124, 124))
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

        self.setIconSize(QSize(150, 150))
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setFlow(QListView.LeftToRight)
        self.setSortingEnabled(True)
        # self.setMovement(QListView.Static)
        self.setWrapping(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ThumbListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            super(ThumbListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(SIGNAL("dropped"), links)
        else:
            event.setDropAction(Qt.CopyAction)
            super(ThumbListWidget, self).dropEvent(event)


class TestDialog(QDialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        self.asset_list_widget = ThumbListWidget()
        self.asset_list_widget.setAcceptDrops(False)
        self.include_list_widget = ThumbListWidget()
        main_layout.addWidget(self.asset_list_widget)
        main_layout.addWidget(self.include_list_widget)
        self.init()

    def init(self):
        for i in ["Render26", "Render27", "Render36", "Render37B"]:
            item = QListWidgetItem(i)
            icon_path = os.path.normpath(os.path.join("D:/pictures", i))
            item.setIcon(QIcon(icon_path))
            self.asset_list_widget.addItem(item)


app = QApplication(sys.argv)
td = TestDialog()
td.show()
app.exec_()


if __name__ == "__main__":
    pass
