# -*- coding: utf-8 -*-
import sys
from PySide import QtGui
from ..libs import get_icon_path


class SystemTray(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        super(SystemTray, self).__init__(parent)
        self.setToolTip("APP Manager")
        self.set_icon()
        self.create_actions()
        self.create_tray_menu()

    def set_icon(self, icon_path=None):
        if not icon_path:
            icon_path = get_icon_path.get_icon_path("app.png")
        icon = QtGui.QIcon(icon_path)
        self.setIcon(icon)

    def create_actions(self):
        """
        button = QtGui.QPushButton()
        palette = self.button.palette()
        role = self.button.backgroundRole() #choose whatever you like
        palette.setColor(role, QColor('red'))
        button.setPalette(palette)
        self.button.setAutoFillBackground(True)
        :return:
        """
        self.quit_action = QtGui.QAction("quit", self)
        self.show_action = QtGui.QAction("show", self)

    def create_tray_menu(self):
        self.tray_menu = QtGui.QMenu()
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.quit_action)
        self.setContextMenu(self.tray_menu)

    def quit(self):
        self.deleteLater()
        sys.exit(0)
