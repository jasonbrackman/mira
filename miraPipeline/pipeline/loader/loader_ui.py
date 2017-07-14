# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from miraFramework.Filter import ButtonLineEdit
from miraFramework.waiting import Waiting


class ThumbListView(QListView):
    def __init__(self, parent=None):
        super(ThumbListView, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setFlow(QListView.LeftToRight)
        self.setMovement(QListView.Static)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWrapping(True)
        self.setSpacing(25)


class LoaderUI(QMainWindow):
    def __init__(self, parent=None):
        super(LoaderUI, self).__init__(parent)
        self.setWindowTitle("Loader")
        self.resize(570, 690)
        self.setWindowFlags(Qt.Window)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)

        project_layout = QHBoxLayout()
        project_layout.setContentsMargins(0, 0, 0, 0)
        project_label = QLabel("Project")
        project_label.setFixedWidth(50)
        self.project_cbox = QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        self.entity_tab = QTabWidget()
        asset_widget = QWidget()
        self.asset_layout = QHBoxLayout(asset_widget)
        self.asset_layout.setAlignment(Qt.AlignTop)
        self.asset_btn_grp = QButtonGroup()
        self.asset_btn_grp.setExclusive(True)
        self.entity_tab.addTab(asset_widget, "Asset")
        self.entity_tab.setMaximumHeight(60)

        shot_widget = QWidget()
        #todo: add shot
        self.entity_tab.addTab(shot_widget, "Shot")

        filter_layout = QHBoxLayout()
        self.filter_le = ButtonLineEdit()
        filter_layout.addStretch()
        filter_layout.addWidget(self.filter_le)

        self.list_view = ThumbListView()
        show_layout = QHBoxLayout()
        show_label = QLabel("Current Selected:")
        self.show_le = QLineEdit()
        self.show_le.setReadOnly(True)
        self.show_le.setStyleSheet("border: 0px solid;")
        show_layout.addWidget(show_label)
        show_layout.addWidget(self.show_le)

        main_layout.addLayout(project_layout)
        main_layout.addWidget(self.entity_tab)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.list_view)
        main_layout.addLayout(show_layout)

        self.waiting_widget = Waiting(self.list_view)
        self.waiting_widget.hide()


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(LoaderUI)
