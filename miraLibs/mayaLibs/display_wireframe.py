# -*- coding: utf-8 -*-
import maya.cmds as mc


def display_wireframe(*args):
    model_panels = mc.getPanel(type="modelPanel")
    for currentPanel in model_panels:
        mc.modelEditor(currentPanel, e=True, displayAppearance='wireframe')
