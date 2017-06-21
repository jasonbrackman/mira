# -*- coding: utf-8 -*-
import os
import shutil
import getpass
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from ..libs import get_icon_path
from ..libs.conf_parser import ConfParser
from ..libs import get_conf_path


class UserDisplay(QWidget):
    def __init__(self, parent=None):
        super(UserDisplay, self).__init__(parent)
        self.setFixedHeight(36)
        self.setup_ui()
        self.menu = QMenu(self)
        self.set_user_picture_action = QAction("User Picture(.png)", self)
        self.add_tool_action = QAction("Add Tools", self)
        self.insert_tool_action = QAction("Insert Tools", self)
        self.collapse_all_action = QAction("Collapse All/Expand All", self)
        self.reset_action = QAction("Reset", self)

        self.set_menu_btn_icon()
        self.set_user_icon()
        self.set_user_name()
        self.set_signals()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 10, 0)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(35, 35)
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignCenter)
        self.menu_btn = QToolButton()
        self.menu_btn.setStyleSheet("background-color: #555555; border:0px solid;border-radius: 2px;")
        main_layout.addStretch()
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.text_label)
        main_layout.addStretch()
        main_layout.addWidget(self.menu_btn)

    def set_signals(self):
        self.menu_btn.clicked.connect(self.create_menu)
        self.set_user_picture_action.triggered.connect(self.set_user_picture)

    @staticmethod
    def get_user_icon_conf_path():
        user_icon_conf_path = get_conf_path.get_conf_path("user_icon_path.yml")
        return user_icon_conf_path

    def set_user_pixmap(self, pixmap_path):
        pixmap = QPixmap(pixmap_path)
        label_width = self.icon_label.width()
        label_height = self.icon_label.height()
        image_width = pixmap.width()
        image_height = pixmap.height()
        if image_width > image_height:
            scaled = pixmap.scaled(QSize(label_width, image_width/label_width*image_height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            scaled = pixmap.scaled(QSize(label_height/label_height*image_width, label_height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled)
        self.icon_label.setAlignment(Qt.AlignCenter)

    def set_user_icon(self):
        user_icon_conf_path = self.get_user_icon_conf_path()
        if not os.path.isfile(user_icon_conf_path):
            icon_path = get_icon_path.get_icon_path("user_default.png")
        else:
            cp = ConfParser(user_icon_conf_path)
            data = cp.parse().get()
            if data. has_key("user_icon_path"):
                icon_path = data["user_icon_path"]
            else:
                icon_path = get_icon_path.get_icon_path("user_default.jpg")
        self.set_user_pixmap(icon_path)

    def set_user_name(self):
        user_name = getpass.getuser().capitalize()
        self.text_label.setText("<font face='Microsoft YaHei' size=4><b>%s</b></font>" % user_name)

    def set_menu_btn_icon(self):
        arrow_path = get_icon_path.get_icon_path("arrow_drop_down.png")
        self.menu_btn.setIcon(QIcon(arrow_path))

    def create_menu(self):
        self.menu.clear()
        self.menu.addAction(self.set_user_picture_action)
        self.menu.addAction(self.add_tool_action)
        self.menu.addAction(self.insert_tool_action)
        self.menu.addAction(self.collapse_all_action)
        self.menu.addAction(self.reset_action)
        self.menu.exec_(QCursor.pos())

    def set_user_picture(self):
        path, _filter = QFileDialog.getOpenFileName(self, "User Picture", "", "Image Files (*.png)")
        if not path:
            return
        conf_dir = os.path.dirname(get_conf_path.get_app_conf_dir())
        icon_path = os.path.join(conf_dir, os.path.basename(path)).replace("\\", "/")
        shutil.copy(path, icon_path)
        self.set_user_pixmap(icon_path)
        data = dict(user_icon_path=icon_path)
        user_icon_conf_path = str(self.get_user_icon_conf_path())
        cp = ConfParser(user_icon_conf_path)
        cp.parse().set(data)
