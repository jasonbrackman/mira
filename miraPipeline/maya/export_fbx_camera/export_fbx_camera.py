# -*- coding: utf-8 -*-
import os
import subprocess
from Qt.QtWidgets import *
from Qt.QtCore import *
from miraFramework.combo import combo, project_combo
from miraLibs.stLibs import St
from miraLibs.pipeLibs import Project, pipeFile


class Label(QLabel):
    def __init__(self, name=None, parent=None):
        super(Label, self).__init__(parent)
        self.name = name
        self.setText(self.name)
        self.setFixedWidth(60)
        self.setAlignment(Qt.AlignRight)


class ExportFbxCamera(QDialog):
    def __init__(self, parent=None):
        super(ExportFbxCamera, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Export fbx camera")
        self.resize(300, 200)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(10)

        entity_layout = QGridLayout()
        project_label = Label("Project")
        self.project_combo = project_combo.ProjectCombo()
        sequence_label = Label("Sequence")
        self.sequence_le = QLineEdit()
        shot_label = Label("Shot")
        self.shot_le = QLineEdit()
        step_label = Label("Step")
        self.step_combo = combo.CombBox()
        task_label = Label("Task")
        self.task_le = QLineEdit()

        entity_layout.addWidget(project_label, 0, 0)
        entity_layout.addWidget(self.project_combo, 0, 1)
        entity_layout.addWidget(sequence_label, 1, 0)
        entity_layout.addWidget(self.sequence_le, 1, 1)
        entity_layout.addWidget(shot_label, 2, 0)
        entity_layout.addWidget(self.shot_le, 2, 1)
        entity_layout.addWidget(step_label, 3, 0)
        entity_layout.addWidget(self.step_combo, 3, 1)
        entity_layout.addWidget(task_label, 4, 0)
        entity_layout.addWidget(self.task_le, 4, 1)
        entity_layout.setSpacing(10)

        self.export_btn = QPushButton("Export .fbx camera")
        self.export_btn.setMinimumHeight(30)
        main_layout.addLayout(entity_layout)
        main_layout.addWidget(self.export_btn)

        self.init()
        self.set_signals()

    @property
    def project(self):
        return self.project_combo.currentText()

    @property
    def sequence(self):
        return self.sequence_le.text()

    @property
    def shot(self):
        return self.shot_le.text()

    @property
    def step(self):
        return self.step_combo.currentText()

    @property
    def task(self):
        return self.task_le.text()

    def init(self):
        self.db = St.St(self.project)
        self.init_sequence()
        self.init_step()

    def set_signals(self):
        self.sequence_le.editingFinished.connect(self.init_shot)
        self.step_combo.currentIndexChanged.connect(self.set_task)
        self.project_combo.currentIndexChanged.connect(self.on_project_changed)
        self.export_btn.clicked.connect(self.on_export)

    def on_project_changed(self):
        self.sequence_le.setText("")
        self.shot_le.setText("")
        self.init()
        self.task_le.setText("")

    def init_sequence(self):
        sequences = self.db.get_all_sequences()
        if not sequences:
            return
        sequences.sort()
        completer = QCompleter(sequences)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.sequence_le.setCompleter(completer)

    def init_shot(self):
        shots = self.db.get_all_shots(self.sequence)
        if not shots:
            return
        shots = [shot.get("code").split("_")[-1] for shot in shots]
        shots.sort()
        completer = QCompleter(shots)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.shot_le.setCompleter(completer)

    def init_step(self):
        shot_steps = Project(self.project).shot_steps
        self.step_combo.addItems(shot_steps)
        self.step_combo.setCurrentIndex(self.step_combo.count()+1)

    def set_task(self):
        self.task_le.setText(self.step)

    def on_export(self):
        cache_dir = pipeFile.get_task_file(self.project, self.sequence, self.shot, self.step, self.task, "maya_shot_cache")
        camera_cache_path = "%s/camera.abc" % cache_dir
        if not os.path.isfile(camera_cache_path):
            QMessageBox.critical(None, "Warming Tip", u"没有摄像机的.abc缓存文件")
            return
        frame_range = self.db.get_shot_task_frame_range("%s_%s" % (self.sequence, self.shot))
        if not frame_range:
            QMessageBox.critical(None, "Warming Tip", u"strack上没有设置该镜头的帧范围")
            return
        start, end = [int(i) for i in frame_range.split("-")]
        py_path = os.path.abspath(os.path.join(__file__, "..", "export_in_maya.py"))
        py_path = py_path.replace("\\", "/")
        mayabatch = Project(self.project).mayabatch_path
        cmd = "\"%s\" -command \"python \\\"file_name='%s';start=%s;end=%s;execfile('%s')\\\"\"" % (mayabatch, camera_cache_path, start, end, py_path)
        print cmd
        subprocess.Popen(cmd, shell=True)
        QMessageBox.information(None, "Warming Tip", u"开始导出，稍后会将路径弹出。")


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(ExportFbxCamera)
