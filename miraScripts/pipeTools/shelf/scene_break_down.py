# -*- coding: utf-8 -*-
import pymel.core as pm
from PySide import QtGui
from miraScripts.pipeTools.scene_break_down import scene_break_down


def main():
    references = pm.listReferences()
    if not references:
        QtGui.QMessageBox.warning(None, "Warning", "No reference detected")
        return
    scene_break_down.main()
