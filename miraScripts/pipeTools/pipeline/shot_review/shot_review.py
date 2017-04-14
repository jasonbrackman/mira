# -*- coding: utf-8 -*-
import os
import subprocess
from PySide import QtGui, QtCore
from miraLibs.pipeLibs import pipeMira, pipeFile
reload(pipeFile)
from miraLibs.pipeLibs.pipeDb import sql_api


class ListWidget(QtGui.QListWidget):
    def __init__(self, removable=False, parent=None):
        super(ListWidget, self).__init__(parent)
        self.removable = removable
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSortingEnabled(True)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.init()

    def init(self):
        if self.removable:
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        global_pos = self.mapToGlobal(pos)
        menu = QtGui.QMenu(self)
        remove_action = QtGui.QAction("Remove", self)
        remove_action.triggered.connect(self.remove_selection)
        remove_all_action = QtGui.QAction("Remove All", self)
        remove_all_action.triggered.connect(self.remove_all)
        menu.addAction(remove_action)
        menu.addAction(remove_all_action)
        menu.exec_(global_pos)

    def remove_selection(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.takeItem(self.row(item))

    def remove_all(self):
        self.clear()

    def mousePressEvent(self, event):
        point = event.pos()
        item = self.itemAt(point)
        if not item:
            self.clearSelection()
        super(ListWidget, self).mousePressEvent(event)


class MyGroup(QtGui.QGroupBox):
    def __init__(self, label_name=None, check_name=None, parent=None):
        super(MyGroup, self).__init__(parent)
        self.label_name = label_name
        self.check_name = check_name
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(0, 0, 0, 0)
        name_label = QtGui.QLabel()
        name_label.setText('<b>%s</b>' % self.label_name)
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.check_box = QtGui.QCheckBox(self.check_name)
        self.list_widget = ListWidget(False, self)
        main_layout.addWidget(name_label)
        main_layout.addWidget(self.check_box)
        main_layout.addWidget(self.list_widget)
        self.check_box.stateChanged.connect(self.on_check_state_changed)

    def on_check_state_changed(self):
        if self.check_box.isChecked():
            self.list_widget.setEnabled(False)
        else:
            self.list_widget.setEnabled(True)
        self.list_widget.clearSelection()


class ShotReview(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ShotReview, self).__init__(parent)
        self.resize(800, 730)
        self.setWindowTitle("Shot Review")
        self.setWindowFlags(QtCore.Qt.Window)
        self.__projects = pipeMira.get_projects()
        self.current_project = pipeMira.get_current_project()
        self.__db = sql_api.SqlApi(self.current_project)
        self.__shot_context = pipeMira.get_shot_step()
        self.play_list = list()

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        project_layout = QtGui.QHBoxLayout()
        project_label = QtGui.QLabel("Project")
        self.project_cbox = QtGui.QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)
        project_layout.setStretchFactor(project_label, 0)
        project_layout.setStretchFactor(self.project_cbox, 1)

        list_layout = QtGui.QHBoxLayout()

        self.sequence_group = MyGroup("sequence", "All Sequences", self)
        self.sequence_group.check_box.setEnabled(False)
        self.sequence_group.list_widget.setSelectionMode(QtGui.QListWidget.SingleSelection)
        self.shot_group = MyGroup("shot", "All Shots", self)
        self.context_group = MyGroup("context", "Latest", self)
        self.context_group.list_widget.setSelectionMode(QtGui.QListWidget.SingleSelection)

        list_layout.addWidget(self.sequence_group)
        list_layout.addWidget(self.shot_group)
        list_layout.addWidget(self.context_group)

        btn_layout = QtGui.QHBoxLayout()
        self.add_to_playlist_btn = QtGui.QPushButton("Add to playlist")
        btn_layout.addStretch()
        btn_layout.addWidget(self.add_to_playlist_btn)

        self.play_list = ListWidget(True, self)

        play_layout = QtGui.QHBoxLayout()
        self.play_btn = QtGui.QPushButton("Play")
        play_layout.addStretch()
        play_layout.addWidget(self.play_btn)

        main_layout.addLayout(project_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.play_list)
        main_layout.addLayout(play_layout)

        self.init_project()
        self.init_sequence()
        self.set_signals()
        self.set_style()

    def set_style(self):
        qss_path = os.path.abspath(os.path.join(__file__, "..", "style.qss"))
        qss_path = qss_path.replace("\\", "/")
        self.setStyle(QtGui.QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

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
        self.shot_group.check_box.stateChanged.connect(self.on_shot_clicked)
        self.add_to_playlist_btn.clicked.connect(self.add_to_playlist)
        self.play_btn.clicked.connect(self.play)

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
        self.shot_group.check_box.setChecked(False)
        self.shot_group.list_widget.clear()
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
            items = [str(item.text()) for item in items]
            items.sort()
            return items
        else:
            items = custom_group.list_widget.selectedItems()
            if not items:
                return
            items = [str(item.text()) for item in items]
            items.sort()
        return items

    def parse_selected(self):
        play_list = list()
        project = str(self.project_cbox.currentText())
        sequence = self.get_selected_in_group(self.sequence_group)
        shots = self.get_selected_in_group(self.shot_group)
        context_list = self.get_selected_in_group(self.context_group)
        if not all((sequence, shots, context_list)):
            return
        for seq in sequence:
            for shot in shots:
                if context_list == ["newest"]:
                    context_list = ["comp", "lgt", "sim", "anim", "lay"]
                for context in context_list:
                    video = pipeFile.get_shot_step_video_file(seq, shot, context, project)
                    if video and os.path.isfile(video):
                        play_list.append(video)
                        break
        return play_list

    def add_to_playlist(self):
        play_list = self.parse_selected()
        if not play_list:
            return
        else:
            self.play_list.addItems(play_list)

    def play(self):
        items = [self.play_list.item(i) for i in xrange(self.play_list.count())]
        if not items:
            return
        play_list = [str(item.text()) for item in items]
        cmd_str = "rv %s" % " ".join(play_list)
        subprocess.Popen(cmd_str, shell=True)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    sr = ShotReview()
    sr.show()
    app.exec_()
