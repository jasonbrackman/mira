# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore


class ConfigureCommand(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ConfigureCommand, self).__init__(parent)
        self.resize(500, 100)
        self.result = None
        main_layout = QtGui.QGridLayout(self)
        name_label = QtGui.QLabel("Name")
        self.name_le = QtGui.QLineEdit()
        command_label = QtGui.QLabel("Command")
        self.command_le = QtGui.QLineEdit()
        btn_layout = QtGui.QHBoxLayout()
        self.ok_btn = QtGui.QPushButton("OK")
        self.cancel_btn = QtGui.QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addWidget(name_label, 0, 0, 1, 1)
        main_layout.addWidget(self.name_le, 0, 1, 1, 6)
        main_layout.addWidget(command_label, 1, 0, 1, 1)
        main_layout.addWidget(self.command_le, 1, 1, 1, 6)
        main_layout.addLayout(btn_layout, 2, 1, 1, 6)
        self.set_signals()

    def set_signals(self):
        self.cancel_btn.clicked.connect(self.do_close)
        self.ok_btn.clicked.connect(self.get_result)

    def do_close(self):
        self.close()
        self.deleteLater()

    def get_result(self):
        name = str(self.name_le.text())
        command = str(self.command_le.text())
        if not all((name, command)):
            return
        self.result = {name: command}
        self.close()


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    sc = ConfigureCommand()
    sc.show()
    app.exec_()


if __name__ == "__main__":
    main()
