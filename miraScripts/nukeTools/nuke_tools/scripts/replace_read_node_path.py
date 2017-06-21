#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/12/7
# version     :
# usage       :
# notes       :

# Built-in modules
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
# Third-party modules
import nuke
# Studio modules

# Local modules


class ReplacePath(QDialog):
    def __init__(self, parent=None):
        super(ReplacePath, self).__init__(parent)
        self.resize(500, 100)
        self.setWindowTitle('Replace Read Node Path')
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        source_label = QLabel('Source Path')
        self.source_le = QLineEdit()
        target_label = QLabel('Target Path')
        self.target_le = QLineEdit()
        self.replace_btn = QPushButton('Replace')
        self.replace_btn.clicked.connect(self.do_replace)

        source_layout = QHBoxLayout()
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_le)

        target_layout = QHBoxLayout()
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target_le)

        main_layout.addLayout(source_layout)
        main_layout.addLayout(target_layout)
        main_layout.addWidget(self.replace_btn)

    def do_replace(self):
        source_path = str(self.source_le.text())
        target_path = str(self.target_le.text())
        for node in nuke.allNodes('Read'):
            node_file_path = node['file'].getValue()
            if source_path in node_file_path:
                new_path = node_file_path.replace(source_path, target_path)
                node['file'].setValue(new_path)


def main():
    app = QApplication.instance()
    global rp
    try:
        rp.close()
        rp.deleteLater()
    except:pass
    nuke_win = app.activeWindow()
    rp = ReplacePath(nuke_win)
    rp.show()

if __name__ == '__main__':
    main()
