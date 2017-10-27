# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from get_icon import get_icon
import pipeGlobal
from miraFramework.Filter import Filter
from miraLibs.pyLibs import join_path


class ReplaceUI(QDialog):
    def __init__(self, parent=None):
        super(ReplaceUI, self).__init__(parent)
        self.setWindowTitle("Replace Rig Reference")
        self.setWindowFlags(Qt.Window)
        self.green_icon_path = get_icon(True)
        self.red_icon_path = get_icon(False)
        self.resize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        proxy_filter_layout = QHBoxLayout()
        self.filter_le = Filter()
        proxy_filter_layout.addStretch()
        proxy_filter_layout.addWidget(self.filter_le)
        self.update_btn = QToolButton()
        icon_path = join_path.join_path2(pipeGlobal.icons_dir, "update.png")
        self.update_btn.setIcon(QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;}"
                                      "QToolButton::hover{background:#00BFFF;border-color:#00BFFF;}")
        proxy_filter_layout.addWidget(self.update_btn)
        
        self.table_view = QTableView()
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        btn_layout = QHBoxLayout()
        self.switch_btn = QPushButton("Switch")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.switch_btn)
        btn_layout.addWidget(self.cancel_btn)
        # --filter layout
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_group = QGroupBox()
        filter_layout.addWidget(filter_group)
        check_layout = QHBoxLayout(filter_group)
        check_layout.setContentsMargins(3, 1, 0, 1)
        filter_label = QLabel("Filters")
        self.check_btn_group = QButtonGroup()
        self.check_btn_group.setExclusive(False)
        self.green_check = QCheckBox()
        self.green_check.setChecked(True)
        self.green_check.setIcon(QIcon(self.green_icon_path))
        self.red_check = QCheckBox()
        self.red_check.setChecked(True)
        self.red_check.setIcon(QIcon(self.red_icon_path))
        check_layout.addWidget(filter_label)
        check_layout.addWidget(self.green_check)
        check_layout.addWidget(self.red_check)
        self.check_btn_group.addButton(self.green_check)
        self.check_btn_group.addButton(self.red_check)

        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(filter_layout)
        bottom_layout.addStretch()
        bottom_layout.addLayout(btn_layout)

        main_layout.addLayout(proxy_filter_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(bottom_layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ru = ReplaceUI()
    ru.show()
    app.exec_()
