# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.OpenMaya as OpenMaya
from miraLibs.mayaLibs.MayaToolBar import MayaToolBar
from miraLibs.pipeLibs import pipeMira, pipeHistory
from miraLibs.mayaLibs import get_maya_globals
from miraLibs.pipeLibs.pipeMaya import get_current_project
import miraCore


def get_current_project_from_outside():
    current_project = pipeHistory.get("currentProject")
    if not current_project:
        current_project = pipeMira.get_current_project()
    return current_project


def add_project_to_maya_globals(project_object):
    maya_globals = get_maya_globals.get_maya_globals()
    if not maya_globals.exists("currentProject"):
        maya_globals.add(currentProject=project_object)
    else:
        maya_globals.update(currentProject=project_object)


class ProjectButton(QPushButton):
    def __init__(self, parent=None):
        super(ProjectButton, self).__init__(parent)
        self.projects = pipeMira.get_projects()
        self.project = get_current_project_from_outside()
        self.setFixedHeight(22)
        self.set_icon()
        self.set_style_sheet()
        self.create_menu()
        self.set_project(self.project)
        OpenMaya.MEventMessage.addEventCallback("SceneOpened", self.set_project_when_scene_opened)

    def set_style_sheet(self):
        # self.setStyleSheet("background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
        #                    "stop: 0 purple, stop: 0.5 #FF00FF,"
        #                    "stop: 1.0 purple);"
        #                    "color:#FFFFFF;"
        #                    "text-align:left;"
        #                    "font-size:10pt;"
        #                    "font-family:Microsoft YaHei;"
        #                    "border-radius: 0px;"
        #                    "padding: 1px;"
        #                    "border-style: outset;"
        #                    "border-width: 1px;"
        #                    "border-color: #AA00AA;")
        self.setStyleSheet("QPushButton{background: transparent;color: #ff8c00; "
                           "font-size:10pt;font-family:Microsoft YaHei;border-width:0px;"
                           "border-color: #444444; text-align: left;border-radius: 0px;padding-right: 0px;}"
                           "QPushButton:hover{background: #222222;}")

    def set_icon(self):
        icon_dir = miraCore.get_icons_dir()
        icon_path = os.path.join(icon_dir, "project_icon", "%s.png" % self.project)
        if not os.path.isfile(icon_path):
            icon_path = os.path.join(icon_dir, "project_icon", "company.png")
        icon_path = icon_path.replace("\\", "/")
        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setIconSize(QSize(50, self.height()))

    def create_menu(self):
        self.menu = QMenu()
        for project in self.projects:
            self.action = QAction(project, self)
            self.action.triggered.connect(self.switch_project)
            self.menu.addAction(self.action)
        self.setMenu(self.menu)

    def switch_project(self):
        self.project = self.sender().text()
        self.set_project(self.project)

    def set_project(self, project):
        if project in self.projects:
            self.project = project
            text = u" 当前项目: %s" % self.project
            self.setText(text)
            self.record_history()
            self.set_icon()
        else:
            QMessageBox.warning(None, "Warming Tip", "%s is not a unknown project." % project)

    def record_history(self):
        settings = QSettings("Mira", "History")
        settings.setValue("currentProject", self.project)

    def set_project_when_scene_opened(self, *args):
        current_project = get_current_project.get_current_project()
        self.project = current_project
        self.set_project(self.project)

    def get(self):
        return self.project

    def show(self):
        maya_tool_bar = MayaToolBar()
        maya_tool_bar.add(self)
        add_project_to_maya_globals(self)

    def delete(self):
        self.deleteLater()


def main():
    global pb
    try:
        pb.delete()
    except:pass
    pb = ProjectButton()
    pb.show()


if __name__ == "__main__":
    main()
