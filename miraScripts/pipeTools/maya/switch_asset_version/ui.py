# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from miraFramework.Filter import ButtonLineEdit
import miraCore
from miraLibs.pyLibs import join_path


class ReplaceAssetUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ReplaceAssetUI, self).__init__(parent)
        self.resize(1000, 600)
        self.setWindowTitle("Replace asset version")
        self.setObjectName("Replace Asset Version")
        self.setup_ui()
        self.setWindowFlags(QtCore.Qt.Window)

    def setup_ui(self):
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 2, 0, 0)
        top_layout = QtGui.QHBoxLayout()

        self.select_check = QtGui.QCheckBox("Select in Maya")
        self.select_check.setChecked(True)

        self.filter_le = ButtonLineEdit()
        self.filter_le.setPlaceholderText("Search...")
        self.update_btn = QtGui.QToolButton()
        icon_path = join_path.join_path2(miraCore.get_icons_dir(), "update.png")
        self.update_btn.setIcon(QtGui.QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;border: 0px;}"
                                      "QToolButton::hover{background:#AAAAAA;}")

        top_layout.addWidget(self.select_check)
        top_layout.addStretch()
        top_layout.addWidget(self.filter_le)
        top_layout.addWidget(self.update_btn)

        self.tree_view = QtGui.QTreeView()

        btn_layout = QtGui.QHBoxLayout()
        self.replace_btn = QtGui.QPushButton("Replace")
        self.replace_btn.setFixedHeight(30)
        btn_layout.addWidget(self.replace_btn)

        # main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tree_view)
        # main_layout.addLayout(btn_layout)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    rau = ReplaceAssetUI()
    rau.show()
    app.exec_()




