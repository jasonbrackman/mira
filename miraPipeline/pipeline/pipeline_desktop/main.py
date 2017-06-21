# -*- coding: utf-8 -*-
import sys
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from python.ui import system_tray


def main():
    app = QApplication(sys.argv)
    tray = system_tray.SystemTray()
    tray.show()
    tray.show_message("Hey,welcome here.\n\nAny questions,connect TD,Thank you! ")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
