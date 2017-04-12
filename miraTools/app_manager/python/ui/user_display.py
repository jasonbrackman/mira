# -*- coding: utf-8 -*-
import os
import getpass
from PySide import QtGui, QtCore
from ..libs import get_icon_path
from ..libs.conf_parser import ConfParser
from ..libs import get_conf_path


class UserDisplay(QtGui.QWidget):
    def __init__(self, parent=None):
        super(UserDisplay, self).__init__(parent)
        self.setFixedHeight(36)
        self.setup_ui()
        self.menu = QtGui.QMenu(self)
        self.set_user_picture_action = QtGui.QAction("User Picture(.png)", self)
        self.add_tool_action = QtGui.QAction("Add Tools", self)
        self.insert_tool_action = QtGui.QAction("Insert Tools", self)
        self.collapse_all_action = QtGui.QAction("Collapse All/Expand All", self)
        self.reset_action = QtGui.QAction("Reset", self)

        self.set_menu_btn_icon()
        self.set_user_icon()
        self.set_user_name()
        self.set_signals()

    def setup_ui(self):
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 10, 0)
        self.icon_label = QtGui.QLabel()
        self.icon_label.setFixedSize(35, 35)
        self.text_label = QtGui.QLabel()
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.menu_btn = QtGui.QToolButton()
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
        pixmap = QtGui.QPixmap(pixmap_path)
        label_width = self.icon_label.width()
        label_height = self.icon_label.height()
        image_width = pixmap.width()
        image_height = pixmap.height()
        if image_width > image_height:
            scaled = pixmap.scaled(QtCore.QSize(label_width, image_width/label_width*image_height), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        else:
            scaled = pixmap.scaled(QtCore.QSize(label_height/label_height*image_width, label_height), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled)
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)

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
        self.menu_btn.setIcon(QtGui.QIcon(arrow_path))

    def create_menu(self):
        self.menu.clear()
        self.menu.addAction(self.set_user_picture_action)
        self.menu.addAction(self.add_tool_action)
        self.menu.addAction(self.insert_tool_action)
        self.menu.addAction(self.collapse_all_action)
        self.menu.addAction(self.reset_action)
        self.menu.exec_(QtGui.QCursor.pos())

    def set_user_picture(self):
        path, filter = QtGui.QFileDialog.getOpenFileName(self, "User Picture", "", "Image Files (*.png)")
        if not path:
            return
        self.set_user_pixmap(path)
        data = dict(user_icon_path=path)
        user_icon_conf_path = str(self.get_user_icon_conf_path())
        cp = ConfParser(user_icon_conf_path)
        cp.parse().set(data)
