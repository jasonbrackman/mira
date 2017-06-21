# -*- coding: utf-8 -*-
import os
from functools import partial
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from . import send_email
from .email_box import emial_box
from ..frameworks import email_button
from ..libs import get_icon_dir


def get_window_icon():
    icon_dir = get_icon_dir.get_icon_dir()
    icon_path = os.path.join(icon_dir, "email.png")
    icon = QIcon(icon_path)
    return icon


class EmailSystemUI(QMainWindow):
    def __init__(self, parent=None):
        super(EmailSystemUI, self).__init__(parent)
        self.resize(1200, 800)
        self.setWindowTitle("Email")
        self.setWindowIcon(get_window_icon())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 2, 0, 0)
        main_group = QGroupBox()
        main_layout.addWidget(main_group)
        main_group_layout = QHBoxLayout(main_group)

        btn_layout = QVBoxLayout()
        btn_group = QGroupBox()
        group_layout = QVBoxLayout(btn_group)
        group_layout.setAlignment(Qt.AlignTop)
        group_layout.setContentsMargins(2, 3, 2, 3)
        self.receive_btn = email_button.EmailButton("receive", u"收件箱")
        self.send_box_btn = email_button.EmailButton("has_send", u"已发送")
        self.recycle_btn = email_button.EmailButton("recycle", u"回收站")
        group_layout.addWidget(self.receive_btn)
        group_layout.addWidget(self.send_box_btn)
        group_layout.addWidget(self.recycle_btn)
        btn_layout.addWidget(btn_group)

        send_group = QGroupBox()
        send_layout = QVBoxLayout(send_group)
        send_layout.setContentsMargins(2, 3, 2, 3)
        send_layout.setAlignment(Qt.AlignTop)
        self.send_btn = email_button.EmailButton("write", u"写信")
        send_layout.addWidget(self.send_btn)
        btn_layout.addWidget(send_group)
        btn_layout.setStretch(1, 1)

        self.display_layout = QStackedLayout()
        self.send_email_widget = send_email.SendEmailUI()
        self.receive_box_widget = emial_box.EmailBox("receiveBox")
        self.send_box_widget = emial_box.EmailBox("sendBox")
        self.recycle_box_widget = emial_box.EmailBox("recycleBox")
        self.display_layout.insertWidget(0, self.send_email_widget)
        self.display_layout.insertWidget(1, self.receive_box_widget)
        self.display_layout.insertWidget(2, self.send_box_widget)
        self.display_layout.insertWidget(3, self.recycle_box_widget)
        self.display_layout.setCurrentIndex(1)

        main_group_layout.addLayout(btn_layout)
        main_group_layout.addLayout(self.display_layout)
        main_group_layout.setStretchFactor(btn_layout, 2)
        main_group_layout.setStretchFactor(self.display_layout, 11)
        main_group_layout.setStretch(0, 0)
        self.set_style()
        self.set_signals()

    def set_style(self):
        qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
        self.setStyleSheet(open(qss_path, 'r').read())

    def set_signals(self):
        self.send_btn.clicked.connect(self.set_current_send_email)
        self.receive_btn.clicked.connect(partial(self.show_email, 1))
        self.send_box_btn.clicked.connect(partial(self.show_email, 2))
        self.recycle_btn.clicked.connect(partial(self.show_email, 3))

    def show_email(self, index):
        current_widget = self.display_layout.widget(index)
        current_widget.set_model()
        try:
            current_widget.show_email(0)
        except:pass
        self.display_layout.setCurrentIndex(index)

    def set_current_send_email(self):
        self.display_layout.setCurrentIndex(0)
        self.send_email_widget.filter_le.setText("")
        self.send_email_widget.title_le.setText("")
        self.send_email_widget.content_te.setText("")
