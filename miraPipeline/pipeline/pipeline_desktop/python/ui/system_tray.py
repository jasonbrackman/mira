# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from functools import partial
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from ..libs import get_icon_dir
from ..libs import get_department_of_user
from ..libs import get_conf_data


def get_tray_icon_path():
    icon_dir = get_icon_dir.get_icon_dir()
    tray_icon_path = os.path.join(icon_dir, "company.png").replace("\\", "/")
    return tray_icon_path


class Action(object):
    def __init__(self, name, command):
        self.name = name
        self.command = command


class SystemTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(SystemTray, self).__init__(parent)
        self.duration = 10000
        self.setToolTip("Pipeline")
        self.set_icon()
        self.create_tray_menu()

    def set_duration(self, value):
        self.duration = value

    def set_icon(self, icon_path=None):
        if not icon_path:
            icon_path = get_tray_icon_path()
        icon = QIcon(icon_path)
        self.setIcon(icon)

    @staticmethod
    def get_actions():
        actions = list()
        department = get_department_of_user.get_department_of_user()
        conf_data = get_conf_data.get_conf_data()
        if not conf_data .__contains__(department):
            print "%s not configured." % department
            return
        department_actions = conf_data[department]
        action_list = sorted(department_actions, key=lambda key: department_actions[key]["order"])
        for each_action in action_list:
            name = department_actions[each_action]["name"]
            command = department_actions[each_action]["command"]
            actions.append(Action(name, command))
        return actions

    @staticmethod
    def run_command(cmd):
        subprocess.Popen(cmd, shell=True)

    def create_tray_menu(self):
        self.tray_menu = QMenu()
        self.tray_menu.setMinimumWidth(150)
        self.tray_menu.setStyleSheet("QMenu{background-color: #FFFFFF;border: 0px solid;font-family: Trebuchet MS;"
                                     "border: 1px solid rgb(110, 110, 110);font-size: 13px;}"
                                     "QMenu::item{background-color: transparent;padding-left: 40px;"
                                     "padding-top: 3px;padding-bottom: 3px;}"
                                     "QMenu::item:selected{color: #FFFFFF;background-color: #708aa2;}")
        actions = self.get_actions()
        if actions:
            for each in actions:
                action = QAction(each.name, self)
                action.triggered.connect(partial(self.run_command, each.command))
                self.tray_menu.addAction(action)
            self.tray_menu.addSeparator()
        self.quit_action = QAction("quit", self)
        self.tray_menu.addAction(self.quit_action)
        self.quit_action.triggered.connect(self.quit)
        self.setContextMenu(self.tray_menu)

    def quit(self):
        self.deleteLater()
        sys.exit(0)

    def show_message(self, title="Warming Tip", msg=""):
        self.showMessage(title, msg, QSystemTrayIcon.Information, self.duration)
