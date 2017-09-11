# -*- coding: utf-8 -*-
import pymel.core as pm
from miraLibs.mayaLibs import get_maya_version


def get_top_shelf():
    return pm.melGlobals['gShelfTopLevel']


def find_shelf_by_name(parent, shelf_name):
    shelf_exists = pm.shelfLayout(shelf_name, exists=True, parent=parent)
    shelf = None
    if shelf_exists:
        shelf = pm.shelfLayout(shelf_name, query=True, fullPathName=True)
    return shelf


def delete_shelf(parent, shelf_name):
    shelf = find_shelf_by_name(parent, shelf_name)
    if shelf:
        pm.deleteUI(shelf)


def create_shelf(parent, shelf_name):
    shelf = pm.shelfLayout(shelf_name, parent=parent, version=get_maya_version.get_maya_version())
    return shelf


def delete_buttons(shelf_name):
    if pm.shelfLayout(shelf_name, q=True, ex=True):
        buttons = pm.shelfLayout(shelf_name, q=True, childArray=True)
        if buttons:
            for button in buttons:
                pm.deleteUI(button)


def create_shelf_button(btn_label, shelf, command, icon_path):
    pm.shelfButton(label=btn_label, parent=shelf, command=command, image1=icon_path)

if __name__ == "__main__":
    pass
