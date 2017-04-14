# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore


class SimReferenceInUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SimReferenceInUI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Sim & Vfx Get Cache")
        self.resize(800, 600)
        main_layout = QtGui.QVBoxLayout(self)
        info_layout = QtGui.QHBoxLayout()
        project_label = QtGui.QLabel("project")
        project_label.setFixedWidth(42)
        self.project_cbox = QtGui.QComboBox()
        self.project_cbox.setEditable(True)
        sequence_label = QtGui.QLabel("sequence")
        sequence_label.setFixedWidth(47)
        self.sequence_le = QtGui.QLineEdit()
        shot_label = QtGui.QLabel("shot")
        shot_label.setFixedWidth(30)
        self.shot_le = QtGui.QLineEdit()
        info_layout.addWidget(project_label)
        info_layout.addWidget(self.project_cbox)
        info_layout.addWidget(sequence_label)
        info_layout.addWidget(self.sequence_le)
        info_layout.addWidget(shot_label)
        info_layout.addWidget(self.shot_le)

        path_layout = QtGui.QHBoxLayout()
        path_label = QtGui.QLabel("Path")
        self.path_le = QtGui.QLineEdit()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_le)

        self.tree_view = QtGui.QTreeView()

        btn_layout = QtGui.QHBoxLayout()
        self.reference_in_btn = QtGui.QPushButton("Reference In")
        btn_layout.addStretch()
        btn_layout.addWidget(self.reference_in_btn)

        main_layout.addLayout(info_layout)
        main_layout.addLayout(path_layout)
        main_layout.addWidget(self.tree_view)
        main_layout.addLayout(btn_layout)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    sri = SimReferenceInUI()
    sri.show()
    app.exec_()
