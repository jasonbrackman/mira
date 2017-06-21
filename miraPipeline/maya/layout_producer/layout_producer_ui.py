# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from miraFramework.Filter import ButtonLineEdit
from miraLibs.pyLibs import join_path
import miraCore


class ThumbListView(QtGui.QListView):
    def __init__(self, parent=None):
        super(ThumbListView, self).__init__(parent)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setViewMode(QtGui.QListView.IconMode)
        self.setResizeMode(QtGui.QListView.Adjust)
        self.setFlow(QtGui.QListView.LeftToRight)
        self.setMovement(QtGui.QListView.Static)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWrapping(True)
        self.setSpacing(15)
        self.menu = QtGui.QMenu()
        self.remove_action = QtGui.QAction("remove", self)
        self.launch_action = QtGui.QAction("Launch Folder", self)
        self.remove_action.triggered.connect(self.remove_item)

    def get_model_data(self):
        model = self.model()
        if isinstance(model, QtGui.QSortFilterProxyModel):
            model = model.sourceModel()
        return model.model_data

    def contextMenuEvent(self, event):
        self.menu.clear()
        self.menu.addAction(self.remove_action)
        self.menu.addAction(self.launch_action)
        self.menu.exec_(QtGui.QCursor.pos())
        event.accept()

    def remove_item(self):
        model = self.model()
        if isinstance(model, QtGui.QSortFilterProxyModel):
            model = model.sourceModel()
        selected_indexes = self.selectedIndexes()
        if not selected_indexes:
            return
        selected_indexes = sorted(selected_indexes, key=lambda index: index.row())
        for index, i in enumerate(selected_indexes):
            model.removeRows(i.row()-index, 1)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove_item()


class LayoutProducerUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LayoutProducerUI, self).__init__(parent)
        self.setWindowTitle("Layout creater")
        self.resize(440, 600)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)

        project_layout = QtGui.QHBoxLayout()
        project_layout.setContentsMargins(10, 2, 10, 2)
        project_label = QtGui.QLabel("Project")
        project_label.setFixedWidth(50)
        self.project_cbox = QtGui.QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        asset_group = QtGui.QGroupBox("asset type")
        asset_layout = QtGui.QHBoxLayout(asset_group)
        self.asset_btn_grp = QtGui.QButtonGroup()
        self.asset_btn_grp.setExclusive(True)
        for asset_type in ["Character", "Prop", "Environment"]:
            self.asset_type_check = QtGui.QCheckBox(asset_type)
            self.asset_btn_grp.addButton(self.asset_type_check)
            asset_layout.addWidget(self.asset_type_check)

        filter_layout = QtGui.QHBoxLayout()
        filter_layout.setContentsMargins(15, 0, 0, 0)
        self.low_check = QtGui.QCheckBox("low")
        self.low_check.setChecked(True)
        namespace_label = QtGui.QLabel("namespace")
        self.name_space_cbox = QtGui.QComboBox()
        self.filter_le = ButtonLineEdit()
        self.update_btn = QtGui.QToolButton()
        icon_path = join_path.join_path2(miraCore.get_icons_dir(), "update.png")
        self.update_btn.setIcon(QtGui.QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;}"
                                      "QToolButton::hover{background:#00BFFF;border-color:#00BFFF;}")
        filter_layout.addWidget(self.low_check)
        filter_layout.addStretch()
        filter_layout.addWidget(namespace_label)
        filter_layout.addWidget(self.name_space_cbox)
        filter_layout.addStretch()
        filter_layout.addWidget(self.filter_le)
        filter_layout.addWidget(self.update_btn)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)

        asset_widget = QtGui.QWidget()
        asset_layout = QtGui.QVBoxLayout(asset_widget)
        asset_layout.setContentsMargins(0, 0, 0, 0)
        self.asset_list_view = ThumbListView()

        add_btn_layout = QtGui.QHBoxLayout()
        self.add_btn = QtGui.QToolButton()
        self.add_btn.setShortcut("Ctrl+D")
        self.add_btn.setToolTip("Ctrl+D")
        icon_dir = miraCore.get_icons_dir()
        arrow_down_path = join_path.join_path2(icon_dir, "arrow_dow.png")
        self.add_btn.setIcon(QtGui.QIcon(arrow_down_path))
        add_btn_layout.addWidget(self.add_btn)
        asset_layout.addWidget(self.asset_list_view)
        asset_layout.addLayout(add_btn_layout)

        self.include_list_view = ThumbListView()

        splitter.addWidget(asset_widget)
        splitter.addWidget(self.include_list_view)

        btn_layout = QtGui.QHBoxLayout()
        self.reference_all_btn = QtGui.QPushButton("Reference All")
        self.reference_sel_btn = QtGui.QPushButton("Reference Selected")
        btn_layout.setSpacing(6)
        btn_layout.addStretch()
        btn_layout.addWidget(self.reference_all_btn)
        btn_layout.addWidget(self.reference_sel_btn)

        main_layout.addLayout(project_layout)
        main_layout.addWidget(asset_group)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(splitter)
        main_layout.addLayout(btn_layout)
        splitter.setSizes([self.height()*0.8, self.height()*0.2])