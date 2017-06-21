# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from ..frameworks import frame_layout, app_button
from ..libs import get_path_from_link, recent_operation


class AppCellWidget(QWidget):
    delete_signal = Signal(basestring)

    def __init__(self, name=None, collapse=False, parent=None):
        super(AppCellWidget, self).__init__(parent)
        self.name = name
        self.collapse = collapse
        self.apps = list()
        self.setup_ui()

    def setup_ui(self):
        self.setAcceptDrops(True)
        self.main_layout = frame_layout.FrameLayout(self.name, self.collapse, True, self)
        self.main_layout.set_btn.clicked.connect(self.set_name)
        self.main_layout.delete_btn.clicked.connect(self.delete_self)
        self.app_grid_layout = QGridLayout(self.main_layout.frame)
        self.app_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.app_grid_layout.setAlignment(Qt.AlignTop)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.setStyleSheet("background: #3e3e3e;")
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("background: #303030;")

    def dropEvent(self, event):
        self.setStyleSheet("background: #303030;")
        for url in event.mimeData().urls():
            temp_path = url.toLocalFile()
            path = get_path_from_link.get_path_from_link(temp_path)
            if not (os.path.isfile(path) or os.path.isdir(path)):
                continue
            default_name = os.path.splitext(os.path.basename(path))[0]
            name, ok = QInputDialog.getText(self, "App Name", "Please input an app name",
                                                  QLineEdit.Normal, default_name)
            if not ok:
                continue
            app_names = [app.name for app in self.apps]
            if name in app_names:
                continue
            self.append_app_btn(name, path)

    def append_app_btn(self, name, path):
        app_btn = app_button.AppButton(name, path, self)
        app_btn.remove_action.triggered.connect(self.refresh_layout)
        app_btn.clicked.connect(self.change_modified_recent)
        max_num = len(self.apps)
        row = max_num / 2
        column = max_num % 2
        self.app_grid_layout.addWidget(app_btn, row, column)
        self.apps.append(app_btn)

    def refresh_layout(self):
        current_app = self.sender().parent()
        self.apps.remove(current_app)
        app_info_list = [[app.name, app.exe_path] for app in self.apps]
        for app in self.apps:
            app.deleteLater()
        self.apps = list()
        for app_info in app_info_list:
            name, path = app_info
            self.append_app_btn(name, path)

    def change_modified_recent(self):
        name = self.sender().name
        exe_path = self.sender().exe_path
        recent_operation.save_to_recent(name, exe_path)

    def set_name(self):
        text, ok = QInputDialog.getText(self, "Group Name", "Please input a group name",
                                              QLineEdit.Normal, self.main_layout.collapse_btn.text())
        if text and ok:
            self.name = text.upper()
            self.main_layout.collapse_btn.setText(self.name)

    def delete_self(self):
        self.delete_signal.emit(self.name.upper())
        self.deleteLater()
