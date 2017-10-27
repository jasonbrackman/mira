# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import pipeGlobal
from miraLibs.pipeLibs.pipeDb import sql_api


class Selected(object):
    pass


class MyGroup(QGroupBox):
    def __init__(self, label_name=None, check_name=None, parent=None):
        super(MyGroup, self).__init__(parent)
        self.label_name = label_name
        self.check_name = check_name
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(0, 0, 0, 0)
        name_label = QLabel()
        name_label.setText('<b>%s</b>' % self.label_name)
        name_label.setAlignment(Qt.AlignCenter)
        self.check_box = QCheckBox(self.check_name)
        self.list_widget = QListWidget()
        self.list_widget.setSortingEnabled(True)
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        main_layout.addWidget(name_label)
        main_layout.addWidget(self.check_box)
        main_layout.addWidget(self.list_widget)
        self.check_box.stateChanged.connect(self.on_check_state_changed)

    def on_check_state_changed(self):
        if self.check_box.isChecked():
            self.list_widget.setEnabled(False)
        else:
            self.list_widget.setEnabled(True)


class PipelineWidget(QDialog):
    play_clicked = Signal(dict)

    def __init__(self, parent=None):
        super(PipelineWidget, self).__init__(parent)
        self.resize(600, 420)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.__projects = pipeGlobal.projects
        self.current_project = pipeGlobal.current_project
        self.__db = sql_api.SqlApi(self.current_project)
        self.__sequence_context = ["lay"]
        self.__shot_context = pipeMira.get_shot_step()
        self.play_list = list()

        main_layout = QVBoxLayout(self)
        project_layout = QHBoxLayout()
        project_label = QLabel("Project")
        self.project_cbox = QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)
        project_layout.setStretchFactor(project_label, 0)
        project_layout.setStretchFactor(self.project_cbox, 1)

        list_layout = QHBoxLayout()

        self.sequence_group = MyGroup("sequence", "All Sequences", self)
        self.sequence_group.check_box.setEnabled(False)
        self.sequence_group.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.shot_group = MyGroup("shot", "All Shots", self)
        self.context_group = MyGroup("context", "Newest", self)
        self.context_group.list_widget.setSelectionMode(QListWidget.SingleSelection)

        list_layout.addWidget(self.sequence_group)
        list_layout.addWidget(self.shot_group)
        list_layout.addWidget(self.context_group)

        btn_layout = QHBoxLayout()
        self.play_btn = QPushButton("Play")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(project_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(btn_layout)

        self.init_project()
        self.init_sequence()
        self.set_signals()

    def init_project(self):
        self.project_cbox.addItems(self.__projects)
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(self.current_project))

    def init_sequence(self):
        sequences = self.__db.getAssetListByAssetType({"assetType": "scene", "assetChildType": None})
        self.sequence_group.list_widget.clear()
        self.sequence_group.list_widget.addItems(sequences)

    def set_signals(self):
        self.project_cbox.currentIndexChanged.connect(self.change_project)
        self.sequence_group.list_widget.itemClicked.connect(self.on_sequence_clicked)
        self.shot_group.list_widget.itemClicked.connect(self.on_shot_clicked)
        self.shot_group.list_widget.itemSelectionChanged.connect(self.on_shot_clicked)
        self.cancel_btn.clicked.connect(self.close)
        self.shot_group.check_box.stateChanged.connect(self.on_shot_clicked)
        self.play_btn.clicked.connect(self.get_play_list)

    def change_project(self, index):
        self.current_project = self.__projects[index]
        self.__db = sql_api.SqlApi(self.current_project)
        self.init_sequence()
        self.shot_group.list_widget.clear()
        self.shot_group.check_box.setChecked(False)

    def on_sequence_clicked(self, item):
        self.context_group.check_box.setChecked(False)
        self.context_group.check_box.setEnabled(False)
        self.context_group.list_widget.clear()
        self.shot_group.list_widget.clear()
        self.context_group.list_widget.addItems(self.__sequence_context)
        arg_dict = {"assetScene": item.text()}
        shots = self.__db.getShotListBySceneName(arg_dict)
        if shots:
            self.shot_group.list_widget.addItems(shots)

    def on_shot_clicked(self):
        self.context_group.check_box.setEnabled(True)
        self.context_group.list_widget.clear()
        self.context_group.list_widget.addItems(self.__shot_context)

    def get_selected_in_group(self, custom_group):
        if custom_group.check_box.isChecked():
            if custom_group is self.context_group:
                return ["newest"]
            items = [custom_group.list_widget.item(i) for i in xrange(custom_group.list_widget.count())]
            if not items:
                return
            items = [item.text() for item in items]
            items.sort()
            return items
        else:
            items = custom_group.list_widget.selectedItems()
            if not items:
                return
            items = [item.text() for item in items]
            items.sort()
        return items

    def get_play_list(self):
        project = self.current_project
        sequence = self.get_selected_in_group(self.sequence_group)[0]
        shots = self.get_selected_in_group(self.shot_group)
        context = self.get_selected_in_group(self.context_group)[0]
        # if context == "lay":
        #     shots = ["c000"]
        play_dict = {"project": project, "sequence": sequence,
                     "shots": ",".join(shots), "context": context}
        self.play_clicked.emit(play_dict)
