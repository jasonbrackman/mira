# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtGui, QtCore
import sim_reference_in_ui
reload(sim_reference_in_ui)
from miraLibs.mayaLibs import create_reference, get_maya_win
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraLibs.pipeLibs.pipeMaya import get_current_project


class SimReferenceIn(sim_reference_in_ui.SimReferenceInUI):
    def __init__(self, parent=None):
        super(SimReferenceIn, self).__init__(parent)
        self.run_app = sys.executable
        # set table view model
        self.model = QtGui.QFileSystemModel()
        self.tree_view.setModel(self.model)
        self.tree_view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tree_view.hideColumn(1)
        self.tree_view.hideColumn(2)
        self.tree_view.hideColumn(3)
        # init info comboBox
        self.init_info_combo()
        # set signals
        self.set_signals()

    def set_signals(self):
        self.project_cbox.currentIndexChanged[str].connect(self.show_path)
        self.sequence_le.textChanged.connect(self.show_path)
        self.shot_le.textChanged.connect(self.show_path)
        self.path_le.textChanged.connect(self.set_model)
        self.reference_in_btn.clicked.connect(self.reference_in)

    def init_info_combo(self):
        projects = pipeMira.get_projects()
        self.project_cbox.addItems(projects)
        current_project = get_current_project.get_current_project()
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(current_project))
        if self.run_app.endswith("maya.exe"):
            obj = pipeFile.PathDetails.parse_path()
            if obj:
                seq = obj.seq
                shot = obj.shot
                self.sequence_le.setText(seq)
                self.shot_le.setText(shot)
                path = pipeFile.get_shot_step_dir(seq, shot, "anim", "_publish", current_project)
                self.path_le.setText(os.path.dirname(path))
                self.set_model(os.path.dirname(path))

    def show_path(self):
        project = self.project_cbox.currentText()
        sequence = self.sequence_le.text()
        shot = self.shot_le.text()
        if all((project, sequence, shot)):
            path = pipeFile.get_shot_step_dir(sequence, shot, "anim", "_publish", project)
            self.path_le.setText(os.path.dirname(path))
        else:
            self.path_le.setText("")

    def set_model(self, path):
        if os.path.isdir(path):
            model_index = self.model.setRootPath(path)
            self.tree_view.setRootIndex(model_index)
            self.tree_view.showColumn(0)
        else:
            for i in xrange(self.model.columnCount()):
                self.tree_view.hideColumn(i)

    def get_selected_path(self):
        selection_model = self.tree_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        if not selected_indexes:
            return
        selected_paths = [self.model.filePath(index)
                          for index in selected_indexes
                          if index.column() == 0]
        return selected_paths

    def reference_in(self):
        paths = self.get_selected_path()
        if not paths:
            return
        if self.run_app.endswith("maya.exe"):
            progress_dialog = QtGui.QProgressDialog('Reference in,Please wait......', 'Cancel', 0, len(paths))
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()
            for index, path in enumerate(paths):
                create_reference.create_reference(path)
                progress_dialog.setValue(index+1)
                if progress_dialog.wasCanceled():
                    break


def main():
    sri = SimReferenceIn(get_maya_win.get_maya_win("PySide"))
    sri.show()
