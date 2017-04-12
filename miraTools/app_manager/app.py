# -*- coding: utf-8 -*-
import sys
import threading
from PySide import QtGui
from python.ui.app_manager import AppManager
from python.ui.system_tray import SystemTray
from python.libs import global_hot_keys
GlobalHotKeys = global_hot_keys.GlobalHotKeys


class AppManagerApp(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.system_tray = SystemTray()
        self.set_signals()

    def set_signals(self):
        self.system_tray.quit_action.triggered.connect(self.quit_app)
        self.system_tray.show_action.triggered.connect(self.show_app_manager_ui)
        self.system_tray.activated.connect(self.show_app_manger)

    def show_app_manger(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.show_app_manager_ui()

    @staticmethod
    @GlobalHotKeys.register(GlobalHotKeys.VK_F, GlobalHotKeys.MOD_ALT)
    def show_app_manager_ui():
        global app_man
        try:
            app_man.close()
            app_man.deleteLater()
        except:pass
        app_man = AppManager()
        app_man.move_to_corner()
        app_man.activateWindow()
        app_man.raise_()
        app_man.show()

    def show(self):
        QtGui.QApplication.setQuitOnLastWindowClosed(False)
        self.system_tray.show()
        self.show_app_manager_ui()
        GlobalHotKeys.listen()
        self.app.exec_()

    def quit_app(self):
        GlobalHotKeys.user32.UnregisterHotKey(None, 0)
        self.system_tray.deleteLater()
        app_man.deleteLater()
        self.app.quit()
        sys.exit(0)


def main():
    am = AppManagerApp()
    am.show()


if __name__ == "__main__":
    main()
