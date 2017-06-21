#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """


import maya.cmds as mc
import pymel.core as pm
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import os


def get_current_renderer():
    return pm.PyNode('defaultRenderGlobals').currentRenderer.get()


def check_phong_shader():
    return mc.ls(type='phong')


def check_tx_texture():
    files = pm.ls(type='file')
    if not files:
        return
    tx_textures = [f.fileTextureName.get() for f in files
                   if os.path.splitext(f.fileTextureName.get())[-1] in ['.jpg', '.jpeg', '.tga', '.tif', '.tiff']]
    return tx_textures


def submit():
    from lightingTools import submit_maya_nuke
    print os.path.abspath(os.path.splitext(submit_maya_nuke.__file__)[0]) + '.py'
    reload(submit_maya_nuke)
    submit_maya_nuke.ui()


def main():
    current_renderer = get_current_renderer()
    message = ''
    if current_renderer == 'arnold':
        if check_phong_shader():
            message += 'Phong shader exist!\n'
        if check_tx_texture():
            message += '.jpg|.jpeg|.tif|.tiff|.tga texture exist!\n'
    if message:
        #message = '<font color=#FF0000 size=3><b> %s </font></b>' % message
        message += '\nDo you want to submit?'
        print message
        ret = QMessageBox.warning(None, 'Warning', message, 'Yes', 'No', 'Cancel')
        if ret == 0:
            submit()
    else:
        submit()

if __name__ == '__main__':
    main()