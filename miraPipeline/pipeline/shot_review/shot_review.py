# -*- coding: utf-8 -*-
import os
import subprocess
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraLibs.pipeLibs import pipeMira, pipeFile
reload(pipeFile)
from miraLibs.stLibs import St


class ListWidget(QListWidget):
    def __init__(self, removable=False, parent=None):
        super(ListWidget, self).__init__(parent)
        self.removable = removable
        self.setFocusPolicy(Qt.NoFocus)
        self.setSortingEnabled(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.init()

    def init(self):
        if self.removable:
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.show_step_menu)

    def show_step_menu(self, pos):
        global_pos = self.mapToGlobal(pos)
        menu = QMenu(self)
        remove_action = QAction("Remove", self)
        remove_action.triggered.connect(self.remove_selection)
        remove_all_action = QAction("Remove All", self)
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


class ShotReview(QDialog):
    def __init__(self, parent=None):
        super(ShotReview, self).__init__(parent)
        self.resize(800, 730)
        self.setWindowTitle("Shot Review")
        self.setWindowFlags(Qt.Window)
        self.__projects = pipeMira.get_projects()
        self.current_project = pipeMira.get_current_project()
        self.__sg = St.St(self.current_project)
        self.__shot_step = pipeMira.get_shot_step()
        self.play_list = list()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
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
        self.step_group = MyGroup("step", "Latest", self)
        self.step_group.list_widget.setSelectionMode(QListWidget.SingleSelection)

        list_layout.addWidget(self.sequence_group)
        list_layout.addWidget(self.shot_group)
        list_layout.addWidget(self.step_group)

        btn_layout = QHBoxLayout()
        self.add_to_playlist_btn = QPushButton("Add to playlist")
        btn_layout.addStretch()
        btn_layout.addWidget(self.add_to_playlist_btn)

        self.play_list = ListWidget(True, self)

        play_layout = QHBoxLayout()
        self.play_btn = QPushButton("Play")
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
        self.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

    def init_project(self):
        self.project_cbox.addItems(self.__projects)
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(self.current_project))

    def init_sequence(self):
        sequences = self.__sg.get_sequence()
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
        self.__sg = St.St(self.current_project)
        self.init_sequence()
        self.shot_group.list_widget.clear()
        self.shot_group.check_box.setChecked(False)

    def on_sequence_clicked(self, item):
        self.step_group.check_box.setChecked(False)
        self.step_group.check_box.setEnabled(False)
        self.step_group.list_widget.clear()
        self.shot_group.check_box.setChecked(False)
        self.shot_group.list_widget.clear()
        shots = self.__sg.get_all_shots_by_sequence(item.text())
        if shots:
            shot_names = [shot["name"] for shot in shots]
            self.shot_group.list_widget.addItems(shot_names)

    def on_shot_clicked(self):
        self.step_group.check_box.setEnabled(True)
        self.step_group.list_widget.clear()
        self.step_group.list_widget.addItems(self.__shot_step)

    def get_selected_in_group(self, custom_group):
        if custom_group.check_box.isChecked():
            if custom_group is self.step_group:
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
        step_list = self.get_selected_in_group(self.step_group)
        if not all((sequence, shots, step_list)):
            return
        for seq in sequence:
            for shot in shots:
                if step_list == ["newest"]:
                    step_list = ["comp", "lgt", "sim", "anim", "lay"]
                for step in step_list:
                    video = pipeFile.get_shot_task_video_file(project, seq, shot, step, step)
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
    app = QApplication(sys.argv)
    sr = ShotReview()
    sr.show()
    app.exec_()
