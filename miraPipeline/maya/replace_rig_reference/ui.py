# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from get_icon import get_icon
import miraCore
from miraFramework.Filter import ButtonLineEdit
from miraLibs.pyLibs import join_path


class ReplaceUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ReplaceUI, self).__init__(parent)
        self.setWindowTitle("Replace Rig Reference")
        self.setWindowFlags(QtCore.Qt.Window)
        self.green_icon_path = get_icon(True)
        self.red_icon_path = get_icon(False)
        self.resize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        proxy_filter_layout = QtGui.QHBoxLayout()
        self.filter_le = ButtonLineEdit()
        proxy_filter_layout.addStretch()
        proxy_filter_layout.addWidget(self.filter_le)
        self.update_btn = QtGui.QToolButton()
        icon_path = join_path.join_path2(miraCore.get_icons_dir(), "update.png")
        self.update_btn.setIcon(QtGui.QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;}"
                                      "QToolButton::hover{background:#00BFFF;border-color:#00BFFF;}")
        proxy_filter_layout.addWidget(self.update_btn)
        
        self.table_view = QtGui.QTableView()
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        btn_layout = QtGui.QHBoxLayout()
        self.switch_btn = QtGui.QPushButton("Switch")
        self.cancel_btn = QtGui.QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.switch_btn)
        btn_layout.addWidget(self.cancel_btn)
        # --filter layout
        filter_layout = QtGui.QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_group = QtGui.QGroupBox()
        filter_layout.addWidget(filter_group)
        check_layout = QtGui.QHBoxLayout(filter_group)
        check_layout.setContentsMargins(3, 1, 0, 1)
        filter_label = QtGui.QLabel("Filters")
        self.check_btn_group = QtGui.QButtonGroup()
        self.check_btn_group.setExclusive(False)
        self.green_check = QtGui.QCheckBox()
        self.green_check.setChecked(True)
        self.green_check.setIcon(QtGui.QIcon(self.green_icon_path))
        self.red_check = QtGui.QCheckBox()
        self.red_check.setChecked(True)
        self.red_check.setIcon(QtGui.QIcon(self.red_icon_path))
        check_layout.addWidget(filter_label)
        check_layout.addWidget(self.green_check)
        check_layout.addWidget(self.red_check)
        self.check_btn_group.addButton(self.green_check)
        self.check_btn_group.addButton(self.red_check)

        bottom_layout = QtGui.QHBoxLayout()
        bottom_layout.addLayout(filter_layout)
        bottom_layout.addStretch()
        bottom_layout.addLayout(btn_layout)

        main_layout.addLayout(proxy_filter_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(bottom_layout)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ru = ReplaceUI()
    ru.show()
    app.exec_()
