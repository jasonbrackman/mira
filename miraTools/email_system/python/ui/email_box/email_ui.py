# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from ...frameworks import text_edit, filter_line_edit


LIST_VIEW_STYLE = "QListView::item:selected " \
                  "{border: 2px solid #4aa6bf; color: #000000; " \
                  "font-style: normal;font-weight:50}" \
                  "QListView::item{border: 1px solid #C0C0C0;background: #f2feff}" \
                  "QListView::item:hover{border: 1px solid #90c6d9;}"  \
                  "QListView::item:selected:active{border: 2px solid #4aa6bf;font-weight:normal}" \
                  "QListView::item:selected:!active{border: 2px solid #C0C0C0;}" \
                  "QListView{outline: none;}"


class EmailUI(QWidget):
    def __init__(self, parent=None):
        super(EmailUI, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.box_label = QLabel()
        self.box_label.setFixedHeight(30)
        main_layout.addWidget(self.box_label)

        email_group = QGroupBox()
        main_layout.addWidget(email_group)
        group_layout = QHBoxLayout(email_group)
        main_splitter = QSplitter(Qt.Horizontal)
        group_layout.addWidget(main_splitter)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_le = filter_line_edit.FilterLineEdit()
        self.email_list_view = QListView()
        self.email_list_view.setSpacing(4)
        self.email_list_view.setStyleSheet(LIST_VIEW_STYLE)
        self.delete_action = QAction("Delete", self)
        self.email_list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.email_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.email_list_view.customContextMenuRequested.connect(self.show_context_menu)
        left_layout.addWidget(self.filter_le)
        left_layout.addWidget(self.email_list_view)
        main_splitter.addWidget(left_widget)

        right_widget = QWidget()
        content_layout = QVBoxLayout(right_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel()
        self.title_label.setFixedHeight(20)

        separator_layout = QHBoxLayout()
        separator_layout.setContentsMargins(0, 2, 0, 0)
        separator_layout.setAlignment(Qt.AlignBottom)
        frame = QFrame()
        frame.setFrameStyle(QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)

        self.content_text = text_edit.TextEdit()
        self.content_text.setReadOnly(True)
        content_layout.addWidget(self.title_label)
        content_layout.addLayout(separator_layout)
        content_layout.addWidget(self.content_text)

        main_splitter.addWidget(right_widget)
        main_splitter.setStretchFactor(0, 3)
        main_splitter.setStretchFactor(1, 11)

    def show_context_menu(self, pos):
        global_pos = self.email_list_view.mapToGlobal(pos)
        menu = QMenu()
        menu.addAction(self.delete_action)
        menu.exec_(global_pos)
