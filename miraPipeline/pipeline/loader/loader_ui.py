# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from miraFramework.Filter import ButtonLineEdit


class ThumbListView(QListView):
    def __init__(self, parent=None):
        super(ThumbListView, self).__init__(parent)
        # self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setFlow(QListView.LeftToRight)
        self.setMovement(QListView.Static)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWrapping(True)
        self.setSpacing(30)


class LoaderUI(QDialog):
    def __init__(self, parent=None):
        super(LoaderUI, self).__init__(parent)
        self.setWindowTitle("Loader")
        self.resize(720, 600)
        self.setWindowFlags(Qt.Window)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)

        project_layout = QHBoxLayout()
        project_layout.setContentsMargins(0, 0, 0, 0)
        project_label = QLabel("Project")
        project_label.setFixedWidth(50)
        self.project_cbox = QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        asset_group = QGroupBox("asset type")
        self.asset_layout = QHBoxLayout(asset_group)
        self.asset_btn_grp = QButtonGroup()
        self.asset_btn_grp.setExclusive(True)

        filter_layout = QHBoxLayout()
        self.filter_le = ButtonLineEdit()
        filter_layout.addStretch()
        filter_layout.addWidget(self.filter_le)

        self.list_view = ThumbListView()

        main_layout.addLayout(project_layout)
        main_layout.addWidget(asset_group)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.list_view)


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(LoaderUI)
