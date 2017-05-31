# -*- coding: utf-8 -*-
import sys
from PySide import QtGui
from python.ui import system_tray


def main():
    app = QtGui.QApplication(sys.argv)
    tray = system_tray.SystemTray()
    tray.show()
    tray.show_message("Hi,welcome here.\n\nAny questions,connect TD,Thank you! ")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
