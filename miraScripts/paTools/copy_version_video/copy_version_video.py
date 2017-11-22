# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from miraFramework.combo import combo, project_combo
from miraLibs.stLibs import St
from miraLibs.pipeLibs import Project, pipeFile
from miraLibs.pyLibs import copy

DST_DIR = "W:/SnowKidTest/playblast/singleshot_playblast"


class Label(QLabel):
    def __init__(self, name=None, parent=None):
        super(Label, self).__init__(parent)
        self.name = name
        self.setText(self.name)
        self.setFixedWidth(60)
        self.setAlignment(Qt.AlignRight)


class CopyVersionVideo(QDialog):
    def __init__(self, parent=None):
        super(CopyVersionVideo, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Copy Video")
        main_layout = QVBoxLayout(self)
        self.resize(300, 160)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(10)

        entity_layout = QGridLayout()
        project_label = Label("Project")
        self.project_combo = project_combo.ProjectCombo()
        sequence_label = Label("Sequence")
        self.sequence_le = QLineEdit()
        step_label = Label("Step")
        self.step_combo = combo.CombBox()

        entity_layout.addWidget(project_label, 0, 0)
        entity_layout.addWidget(self.project_combo, 0, 1)
        entity_layout.addWidget(sequence_label, 1, 0)
        entity_layout.addWidget(self.sequence_le, 1, 1)
        entity_layout.addWidget(step_label, 2, 0)
        entity_layout.addWidget(self.step_combo, 2, 1)
        entity_layout.setSpacing(10)

        self.copy_btn = QPushButton("Copy Video")
        self.copy_btn.setMinimumHeight(30)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()

        main_layout.addLayout(entity_layout)
        main_layout.addWidget(self.copy_btn)
        main_layout.addWidget(self.progress_bar)
        self.init()
        self.set_signals()

    @property
    def project(self):
        return self.project_combo.currentText()

    @property
    def sequence(self):
        return self.sequence_le.text()

    @property
    def step(self):
        return self.step_combo.currentText()

    def init(self):
        self.db = St.St(self.project)
        self.init_sequence()
        self.init_step()

    def set_signals(self):
        self.project_combo.currentIndexChanged.connect(self.on_project_changed)
        self.copy_btn.clicked.connect(self.on_copy_btn_clicked)

    def on_project_changed(self):
        self.sequence_le.setText("")
        self.shot_le.setText("")
        self.init()

    def init_sequence(self):
        sequences = self.db.get_all_sequences()
        if not sequences:
            return
        sequences.sort()
        completer = QCompleter(sequences)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.sequence_le.setCompleter(completer)

    def init_step(self):
        shot_steps = Project(self.project).shot_steps
        self.step_combo.addItems(shot_steps)
        self.step_combo.setCurrentIndex(self.step_combo.count()+1)

    def on_copy_btn_clicked(self):
        if not self.sequence:
            return
        shots = self.db.get_all_shots(self.sequence)
        if not shots:
            return
        shots = [shot.get("code").split("_")[-1] for shot in shots]
        shots.sort()
        self.progress_bar.show()
        self.progress_bar.setRange(0, len(shots))
        for index, shot in enumerate(shots):
            # project, entity_type, asset_type_sequence, asset_name_shot, step, task, version=""
            video_file = pipeFile.get_task_workVideo_file(self.project, "Shot", self.sequence, shot, self.step, self.step)
            if not os.path.isfile(video_file):
                print "%s is not an exist file" % video_file
                continue
            base_name = os.path.basename(video_file)
            dst_file = "%s/%s/%s/%s" % (DST_DIR, self.sequence, self.step, base_name)
            copy.copy(video_file, dst_file)
            print "Copy %s --> %s" % (video_file, dst_file)
            self.progress_bar.setValue(index+1)
        self.progress_bar.hide()


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(CopyVersionVideo)
