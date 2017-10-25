# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import miraCore
from miraLibs.pipeLibs import pipeMira
from miraLibs.pipeLibs import get_current_project


class ProjectModel(QAbstractListModel):
    def __init__(self, model_data, parent=None):
        super(ProjectModel, self).__init__(parent)
        self.model_data = model_data
        self.parent = parent
        self.__icon_dir = miraCore.icons_dir

    def rowCount(self, parent):
        return len(self.model_data)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return
        row = index.row()
        data = self.model_data[row]
        if role == Qt.DisplayRole:
            return data
        elif role == Qt.SizeHintRole:
            return QSize(self.parent.width(), 25)
        elif role == Qt.DecorationRole:
            icon_path = os.path.join(self.__icon_dir, "project_icon", "%s.png" % data)
            if not os.path.isfile(icon_path):
                return
            pix_map = QPixmap(icon_path)
            pix_map = pix_map.scaled(self.parent.height(), self.parent.height(),
                                     Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            return pix_map


class ProjectCombo(QComboBox):
    def __init__(self, parent=None):
        super(ProjectCombo, self).__init__(parent)
        self.__projects = pipeMira.get_projects()
        self.model = ProjectModel(self.__projects, self)
        self.setModel(self.model)
        self.set_current_project()

    def set_current_project(self):
        current_project = get_current_project.get_current_project()
        if current_project in self.__projects:
            self.setCurrentIndex(self.findText(current_project))


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(ProjectCombo)
