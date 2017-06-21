# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import VideoUI
import FileListView
import FileTableView
from utility.get_icon_dir import get_icon_dir


class CollapseButton(QToolButton):
    def __init__(self, name=None, parent=None):
        super(CollapseButton, self).__init__(parent)
        self.name = name
        self.setFixedSize(50, 12)
        self.setStyleSheet("QToolButton{border-radius:2px;background-color:#222222;}"
                           "QToolButton:hover{background-color:#AAAAAA;border-color:#FFFFFF}")
        icon_dir = get_icon_dir()
        icon_path = os.path.join(icon_dir, "%s.png" % self.name)
        self.setIcon(QIcon(icon_path))


class VideoPlayerUI(QMainWindow):
    def __init__(self, parent=None):
        super(VideoPlayerUI, self).__init__(parent)
        self.resize(900, 700)
        self.setWindowTitle("Media Player")
        # create actions
        self.create_action()
        # create menu
        self.create_menu()
        # create status bar
        self.create_status_bar()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(2, 0, 0, 2)
        self.main_splitter = QSplitter(Qt.Vertical)
        self.video = VideoUI.VideoUI(self)
        self.main_splitter.insertWidget(0, self.video)

        bottom_widget = QWidget()
        self.main_splitter.insertWidget(1, bottom_widget)
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setAlignment(Qt.AlignTop)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)

        self.collapse_widget = QWidget()
        collapse_layout = QHBoxLayout(self.collapse_widget)
        collapse_layout.setContentsMargins(0, 0, 0, 0)
        collapse_layout.setAlignment(Qt.AlignCenter)
        self.collapse_btn = CollapseButton("collapse")
        self.collapse_widget.setFixedHeight(self.collapse_btn.height())
        collapse_layout.addWidget(self.collapse_btn)

        self.file_widget = QWidget()
        file_layout = QHBoxLayout(self.file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_splitter = QSplitter(Qt.Horizontal)
        file_layout.addWidget(file_splitter)
        self.file_list = FileListView.FileListView(self)
        self.file_table = FileTableView.FileTableView(self)
        file_splitter.insertWidget(0, self.file_list)
        file_splitter.insertWidget(1, self.file_table)
        file_splitter.setStretchFactor(0, 0)
        file_splitter.setStretchFactor(1, 1)

        self.expand_widget = QWidget()
        expand_layout = QHBoxLayout(self.expand_widget)
        expand_layout.setContentsMargins(0, 0, 0, 0)
        expand_layout.setAlignment(Qt.AlignCenter)
        self.expand_btn = CollapseButton("expand")
        self.expand_widget.setFixedHeight(self.expand_btn.height())
        expand_layout.addWidget(self.expand_btn)

        bottom_layout.addWidget(self.collapse_widget)
        bottom_layout.addWidget(self.file_widget)
        bottom_layout.setStretchFactor(self.collapse_widget, 0)
        bottom_layout.setStretchFactor(self.file_widget, 1)

        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 0)

        main_layout.addWidget(self.main_splitter)
        main_layout.addWidget(self.expand_widget)

        self.collapse_widget.hide()
        self.file_widget.hide()

    def create_action(self):
        self.pipeline_action = QAction("Pipeline", self)
        self.set_frame_ratio_action = QAction("Frame Ratio", self)
        self.switch_to_normal_action = QAction("Normal Mode", self)
        self.exit_action = QAction("exit", self)

    def create_menu(self):
        self.file_menu = QMenu("File", self)
        self.file_menu.addAction(self.set_frame_ratio_action)
        self.file_menu.addAction(self.switch_to_normal_action)
        self.file_menu.addAction(self.exit_action)
        self.pipeline_menu = QMenu("Pipeline", self)
        self.pipeline_menu.addAction(self.pipeline_action)
        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.pipeline_menu)

    def create_status_bar(self):
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Welcome to use...')
