# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraFramework.Filter import Filter
from miraLibs.pyLibs import join_path
import miraCore


class GpuToMdlUI(QDialog):
    def __init__(self, parent=None):
        super(GpuToMdlUI, self).__init__(parent)
        self.resize(400, 300)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 1, 0, 1)
        # filter layout
        filter_layout = QHBoxLayout()
        filter_layout.addStretch()
        self.filter_le = Filter()
        filter_layout.addWidget(self.filter_le)
        self.update_btn = QToolButton()
        icon_path = join_path.join_path2(miraCore.icons_dir, "update.png")
        self.update_btn.setIcon(QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;}"
                                      "QToolButton::hover{background:#00BFFF;border-color:#00BFFF;}")
        filter_layout.addWidget(self.update_btn)
        # table view
        self.table_view = QTableView()
        # button layout
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table_view)
