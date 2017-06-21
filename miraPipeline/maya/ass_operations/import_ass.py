# -*- coding: utf-8 -*-
import os
import functools
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
from miraLibs.mayaLibs import get_maya_win, create_group, add_namespace
reload(add_namespace)
from miraLibs.pipeLibs import pipeMira
from miraLibs.pyLibs import join_path, get_children_file
from miraLibs.pipeLibs.pipeMaya import import_ass


class ImportAssDialog(QDialog):
    def __init__(self, parent=None):
        super(ImportAssDialog, self).__init__(parent)
        self.resize(500, 400)
        self.current_project = None
        self.setWindowTitle("Import Ass.")
        main_layout = QVBoxLayout(self)

        grid_layout = QGridLayout()
        project_label = QLabel("Project")
        self.project_cbox = QComboBox()
        asset_label = QLabel("Asset Name")
        self.asset_cbox = QComboBox()
        grid_layout.addWidget(project_label, 0, 0, 1, 1)
        grid_layout.addWidget(self.project_cbox, 0, 1, 1, 5)
        grid_layout.addWidget(asset_label, 1, 0, 1, 1)
        grid_layout.addWidget(self.asset_cbox, 1, 1, 1, 5)
        grid_layout.setColumnStretch(0, 0)
        grid_layout.setColumnStretch(1, 1)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.file_list.setSortingEnabled(True)

        btn_layout = QHBoxLayout()
        self.import_all_btn = QPushButton("Import All")
        self.import_selected_btn = QPushButton("Import Selected")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.import_selected_btn)
        btn_layout.addWidget(self.import_all_btn)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(btn_layout)

        self.init()
        self.set_signals()

    def set_signals(self):
        self.asset_cbox.currentIndexChanged[str].connect(self.show_ass)
        self.project_cbox.currentIndexChanged.connect(self.change_project)
        self.import_all_btn.clicked.connect(functools.partial(self.import_ass, True))
        self.import_selected_btn.clicked.connect(functools.partial(self.import_ass, False))
        self.cancel_btn.clicked.connect(self.close)

    def init(self):
        projects = pipeMira.get_projects()
        self.project_cbox.addItems(projects)
        self.current_project = pipeMira.get_current_project()
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(self.current_project))
        self.add_env_assets()

    def add_env_assets(self):
        self.asset_cbox.clear()
        root_dir = pipeMira.get_root_dir(self.current_project)
        env_dir = join_path.join_path2(root_dir, self.current_project, "assets", "proxy")
        if not os.path.isdir(env_dir):
            return
        env_assets = os.listdir(env_dir)
        if not env_assets:
            return
        self.asset_cbox.addItems(env_assets)
        self.asset_cbox.setCurrentIndex(self.asset_cbox.count()+1)

    def change_project(self):
        self.current_project = self.project_cbox.currentText()
        self.add_env_assets()

    def show_ass(self, text):
        self.file_list.clear()
        if not text:
            return
        root_dir = pipeMira.get_root_dir(self.current_project)
        ass_dir = join_path.join_path2(root_dir, self.current_project, "assets", "proxy", text, "static")
        if not os.path.isdir(ass_dir):
            return
        ass_files = get_children_file.get_children_file(ass_dir, ".ass")
        for f in ass_files:
            item = QListWidgetItem(os.path.basename(f))
            item.path = f
            self.file_list.addItem(item)

    def get_selected_items(self, get_all=True):
        if get_all:
            items = [self.file_list.item(row) for row in xrange(self.file_list.count())]
        else:
            items = self.file_list.selectedItems()
        return items

    def import_ass(self, import_all=True):
        items = self.get_selected_items(import_all)
        if not items:
            return
        model_group = items[0].path.split("@")[1]
        if not mc.objExists("standin"):
            create_group.create_group("standin")
        pd = QProgressDialog("Ass Importing...", 'Cancel', 0, len(items))
        pd.setWindowModality(Qt.WindowModal)
        pd.setMinimumWidth(350)
        pd.show()
        for index, item in enumerate(items):
            pd.setValue(index)
            if pd.wasCanceled():
                break
            ass_path = item.path
            import_ass.import_my_ass(ass_path)
        # add namespace
        asset_name = model_group.split("_")[1]
        add_namespace.add_namespace(asset_name, model_group)


def main():
    iad = ImportAssDialog(get_maya_win.get_maya_win("PySide"))
    iad.show()


if __name__ == "__main__":
    main()





