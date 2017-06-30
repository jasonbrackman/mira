# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setIconSize(QSize(150, 150))
        self.setFocusPolicy(Qt.NoFocus)
        self.menu = QMenu()
        self.remove_action = QAction("Remove", self)
        self.set_signals()

    def set_signals(self):
        self.remove_action.triggered.connect(self.remove)

    def remove(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            self.add_file_item(path)

    def contextMenuEvent(self, event):
        self.menu.clear()
        self.menu.addAction(self.remove_action)
        self.menu.exec_(QCursor.pos())
        event.accept()

    def all_items_text(self):
        all_items_text = list()
        if self.count():
            for i in xrange(self.count()):
                all_items_text.append(str(self.item(i).text()))
                all_items_text = [item.replace("\\", "/") for item in all_items_text]
        return all_items_text

    def append_file(self, file_path):
        exists = self.all_items_text()
        if file_path in exists:
            return
        # file_info = QFileInfo(file_path)
        # icon_provider = QFileIconProvider()
        # icon = icon_provider.icon(file_info)
        # pixmap = icon.pixmap(512)
        item = QListWidgetItem(file_path)
        item.setSizeHint(QSize(item.sizeHint().width(), 35))
        # item.setIcon(pixmap)
        self.addItem(item)

    def append_dir(self, file_dir):
        all_files = list()
        for root, dirs, files in os.walk(file_dir):
            for f in files:
                all_files.append(os.path.join(root, f))
                all_files = [f.replace('\\', '/') for f in all_files]
        if not all_files:
            return
        for file_path in all_files:
            self.append_file(file_path)

    def add_file_item(self, path):
        if os.path.isfile(path):
            self.append_file(path)
        elif os.path.isdir(path):
            self.append_dir(path)
        else:
            pass
