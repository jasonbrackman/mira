# -*- coding: utf-8 -*-
import pymel.core as pm
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraPipeline.maya.scene_break_down import scene_break_down


def main():
    references = pm.listReferences()
    if not references:
        QMessageBox.warning(None, "Warning", "No reference detected")
        return
    scene_break_down.main()
