# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from ..libs import get_icon_path


class FrameLayout(QVBoxLayout):
    def __init__(self, button_text=None, collapse_status=None, can_set=True, parent=None):
        super(FrameLayout, self).__init__(parent)
        style_sheet_str = "background:transparent;"
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignTop)
        self.setSpacing(0)
        self.button_text = button_text
        self.collapse_status = collapse_status
        self.can_set = can_set
        self.parent = parent

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(0)
        btn_layout.setAlignment(Qt.AlignLeft)
        self.collapse_btn = QToolButton()
        self.collapse_btn.setFixedHeight(25)
        self.collapse_btn.setStyleSheet(style_sheet_str)
        self.collapse_btn.setText(self.button_text)
        self.collapse_btn.setIconSize(QSize(6, 6))
        self.collapse_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.set_btn = QToolButton()
        self.set_btn.setStyleSheet(style_sheet_str)
        setting_icon = QIcon(get_icon_path.get_icon_path("setting.png"))
        self.set_btn.setIcon(setting_icon)

        self.delete_btn = QToolButton()
        self.delete_btn.setStyleSheet(style_sheet_str)
        delete_icon = QIcon(get_icon_path.get_icon_path("delete.png"))
        self.delete_btn.setIcon(delete_icon)

        btn_layout.addWidget(self.collapse_btn)
        if self.can_set:
            btn_layout.addStretch()
            btn_layout.addWidget(self.set_btn)
            btn_layout.addWidget(self.delete_btn)

        self.frame = QFrame()

        self.addLayout(btn_layout)
        self.addWidget(self.frame)
        self.init_settings()
        self.set_signals()

    def init_settings(self):
        if self.collapse_status:
            self.set_collapse()
        else:
            self.set_expand()

    def set_signals(self):
        self.collapse_btn.clicked.connect(self.change_collapse)

    def change_collapse(self):
        self.collapse_status = not self.collapse_status
        self.init_settings()

    def set_collapse(self):
        self.collapse_btn.setArrowType(Qt.RightArrow)
        self.frame.setHidden(True)

    def set_expand(self):
        self.collapse_btn.setArrowType(Qt.DownArrow)
        self.frame.setHidden(False)
