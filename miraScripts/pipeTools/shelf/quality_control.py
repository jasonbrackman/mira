# -*- coding: utf-8 -*-
from miraLibs.pipeLibs.pipeMaya import get_current_project
from miraLibs.mayaLibs import get_maya_win
from miraScripts.pipeTools.task_QC import task_QC_proc


def main():
    parent_win = get_maya_win.get_maya_win("PySide")
    project = get_current_project.get_current_project()
    win = task_QC_proc.TaskQCProc(parent_win, project)
    win.show()
