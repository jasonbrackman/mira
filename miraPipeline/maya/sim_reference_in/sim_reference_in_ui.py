# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class SimReferenceInUI(QDialog):
    def __init__(self, parent=None):
        super(SimReferenceInUI, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Sim & Vfx Get Cache")
        self.resize(800, 600)
        main_layout = QVBoxLayout(self)
        info_layout = QHBoxLayout()
        project_label = QLabel("project")
        project_label.setFixedWidth(42)
        self.project_cbox = QComboBox()
        self.project_cbox.setEditable(True)
        sequence_label = QLabel("sequence")
        sequence_label.setFixedWidth(47)
        self.sequence_le = QLineEdit()
        shot_label = QLabel("shot")
        shot_label.setFixedWidth(30)
        self.shot_le = QLineEdit()
        info_layout.addWidget(project_label)
        info_layout.addWidget(self.project_cbox)
        info_layout.addWidget(sequence_label)
        info_layout.addWidget(self.sequence_le)
        info_layout.addWidget(shot_label)
        info_layout.addWidget(self.shot_le)

        path_layout = QHBoxLayout()
        path_label = QLabel("Path")
        self.path_le = QLineEdit()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_le)

        self.tree_view = QTreeView()

        btn_layout = QHBoxLayout()
        self.reference_in_btn = QPushButton("Reference In")
        btn_layout.addStretch()
        btn_layout.addWidget(self.reference_in_btn)

        main_layout.addLayout(info_layout)
        main_layout.addLayout(path_layout)
        main_layout.addWidget(self.tree_view)
        main_layout.addLayout(btn_layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    sri = SimReferenceInUI()
    sri.show()
    app.exec_()
