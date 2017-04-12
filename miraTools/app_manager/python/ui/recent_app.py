# -*- coding: utf-8 -*-
import os
from PySide import QtGui, QtCore
from ..libs import get_conf_path, conf_parser, recent_operation
from ..frameworks import frame_layout, app_button


class RecentApp(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RecentApp, self).__init__(parent)
        self.setMinimumHeight(110)
        self.setMaximumHeight(110)
        self.setup_ui()
        self.init()

    def setup_ui(self):
        main_layout = frame_layout.FrameLayout("RECENT", False, False, self)
        self.app_layout = QtGui.QHBoxLayout(main_layout.frame)
        self.app_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.app_layout.setContentsMargins(5, 0, 0, 0)
        self.app_layout.setSpacing(21)

    def add_recent_app(self, name, path):
        app_btn = app_button.AppButton(name, path, self, False)
        app_btn.remove_action.triggered.connect(self.remove_from_recent_record)
        app_btn.setMaximumWidth(55)
        app_btn.setMinimumHeight(80)
        app_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        app_btn.set_text()
        self.app_layout.addWidget(app_btn)

    @staticmethod
    def get_recent_app_conf_path():
        recent_app_conf_path = get_conf_path.get_conf_path("recent_app.yml")
        return recent_app_conf_path

    def init(self):
        recent_app_conf_path = self.get_recent_app_conf_path()
        if not os.path.isfile(recent_app_conf_path):
            return
        cp = conf_parser.ConfParser(recent_app_conf_path)
        conf_data = cp.parse().get()
        if not conf_data:
            return
        app_list = conf_data["recent_apps"]
        for app_dict in app_list:
            for app in app_dict:
                path = app_dict[app]
                self.add_recent_app(app, path)

    def remove_from_recent_record(self):
        name = self.sender().parent().name
        recent_operation.remove_from_recent(name)
