# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya.lgt.import_camera import import_camera


class ImportCamera(QDialog):
    def __init__(self, parent=None):
        super(ImportCamera, self).__init__(parent)
        self.resize(300, 150)
        self.setWindowTitle("Import Camera")
        self.setWindowFlags(Qt.Window)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(15)

        grid_layout = QGridLayout()
        project_label = QLabel("Project")
        self.project_le = QLineEdit()
        sequence_label = QLabel("Sequence")
        self.sequence_le = QLineEdit()
        step_label = QLabel("Step")
        self.step_le = QLineEdit()
        grid_layout.addWidget(project_label, 0, 0)
        grid_layout.addWidget(self.project_le, 0, 1)
        grid_layout.addWidget(sequence_label, 1, 0)
        grid_layout.addWidget(self.sequence_le, 1, 1)
        grid_layout.addWidget(step_label, 2, 0)
        grid_layout.addWidget(self.step_le, 2, 1)

        self.import_btn = QPushButton("Import Camera")

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.import_btn)

        self.init()
        self.import_btn.clicked.connect(self.on_btn_clicked)

    def init(self):
        context = pipeFile.PathDetails.parse_path()
        if not context:
            return
        self.project_le.setText(context.project)
        self.sequence_le.setText(context.sequence)
        self.step_le.setText("Anim")

    def on_btn_clicked(self):
        project = self.project_le.text()
        sequence = self.sequence_le.text()
        step = self.step_le.text()
        if not all((project, sequence, step)):
            print "Fill the blank"
            return
        import_camera(project, sequence, step)


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(ImportCamera)


if __name__ == "__main__":
    main()





