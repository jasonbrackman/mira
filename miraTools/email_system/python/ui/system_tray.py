# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtGui
from ..libs import get_icon_dir


def get_tray_icon_path():
    icon_dir = get_icon_dir.get_icon_dir()
    tray_icon_path = os.path.join(icon_dir, "email.png").replace("\\", "/")
    return tray_icon_path


class SystemTray(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        super(SystemTray, self).__init__(parent)
        self.duration = 10000
        self.setToolTip("Email")
        self.set_icon()
        self.create_actions()
        self.create_tray_menu()

    def set_duration(self, value):
        self.duration = value

    def set_icon(self, icon_path=None):
        if not icon_path:
            icon_path = get_tray_icon_path()
        icon = QtGui.QIcon(icon_path)
        self.setIcon(icon)

    def create_actions(self):
        self.quit_action = QtGui.QAction("quit", self)

    def create_tray_menu(self):
        self.tray_menu = QtGui.QMenu()
        self.tray_menu.addAction(self.quit_action)
        self.setContextMenu(self.tray_menu)

    def quit(self):
        self.deleteLater()
        sys.exit(1)

    def show_message(self, title="You have a new message", msg=""):
        self.showMessage(title, msg, QtGui.QSystemTrayIcon.Information, self.duration)


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    st = SystemTray()
    st.show()
    app.exec_()


if __name__ == "__main__":
    main()
