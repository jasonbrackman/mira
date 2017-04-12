#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename    :
#description :
#author      :Yan-Chen Liao
#date        :2015/5/25
#version     :
#usage       :
#notes       :
#==============================================================================

# Built-in modules
import sys
import os
import re
import time

# Third-party modules
from PySide import QtCore, QtGui
import pymel.core as pm
import maya.cmds as cmds

# Studio modules
import linearWorkflowUI
reload(linearWorkflowUI)
# Local modules
#sys.path.insert(0, r'D:\new_td_prod_clone\petunia\python\studio\maya\renderTools\ui')
#import linearWorkflowUI



WINDOW_NAME = 'Maya Color Linear Workflow And Render Setting'


def maya_main_window():
    import maya.OpenMayaUI as apiUI
    from shiboken import wrapInstance
    main_win_ptr = apiUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_win_ptr), QtGui.QWidget)


class linearWorkflowDialog(QtGui.QDialog):

    def __init__(self, parent=maya_main_window()):
    #def __init__(self, parent=None):
        super(linearWorkflowDialog, self).__init__(parent)
        self.setObjectName(WINDOW_NAME)
        self.setWindowTitle(WINDOW_NAME)
        #self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(QtCore.Qt.Window)
        #self.setup_ui()
        self.checkRenderer()
        self.ui = linearWorkflowUI.ui(self)
        self.show()

    def checkRenderer(self):

        if 'mtoa' not in pm.pluginInfo(query=True, listPlugins=True):
            try:
                pm.loadPlugin('mtoa.mll')
            except:
                QtGui.QMessageBox.information(self, 'Fail to Load Arnold Renderer', 'Fail to Load Arnold Renderer!!')
                self.close()
            pm.PyNode("defaultRenderGlobals").currentRenderer.set('arnold')

        try:
            import mtoa.core
            mtoa.core.createOptions()
            pm.PyNode("defaultRenderGlobals").currentRenderer.set('arnold')
            pm.PyNode('defaultArnoldRenderOptions')
            pm.PyNode('defaultArnoldFilter')
        except:
            QtGui.QMessageBox.information(self, 'Loading Arnold Renderer', 'Loading Arnold Done, \npress OK to \nLinear Workflow Check Tool')
            self.close()


def maya_ui():
    import maya.cmds as cmds
    if cmds.window(WINDOW_NAME, exists=True, q=True):
          cmds.deleteUI(WINDOW_NAME)
    dialog = linearWorkflowDialog(parent=maya_main_window())


def normal_ui():
    app = QtGui.QApplication(sys.argv)
    ui = linearWorkflowDialog()
    #ui.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    #normal_ui()
    maya_ui()


'''
# category, alias name, attrname, current value, default value,

#---------------------------------------------------------------
Color Management Preferences
print cmds.colorManagementPrefs(q=True, cmEnabled=True)
True
print cmds.colorManagementPrefs(q=True, renderingSpaceNames=True)
# [u'ACES', u'scene-linear CIE XYZ', u'scene-linear DCI-P3', u'scene-linear Rec 709/sRGB', u'Sharp RGB']
print cmds.colorManagementPrefs(q=True, renderingSpaceName=True)
# scene-linear Rec 709/sRGB
print cmds.colorManagementPrefs(q=True, viewTransformNames=True)
#[u'1.8 gamma', u'2.2 gamma', u'ACES RRT v0.7', u'Bitsquid tone-map', u'Log', u'Raw', u'Rec 709 gamma', u'sRGB gamma']
print cmds.colorManagementPrefs(q=True, viewTransformName=True)
#sRGB gamma
print cmds.colorManagementPrefs(q=True, defaultInputSpaceName=True)
# scene-linear Rec 709/sRGB
print cmds.colorManagementPrefs(q=True, colorManagePots=True)
True

['Color Management Preferences', 'Enable', '', True],
['Color Management Preferences', 'Rendering Space', '', 'scene-linear Rec 709/sRGB'],
['Color Management Preferences', 'View Transform', '', 'sRGB gamma'],
['Color Management Preferences', 'Default Input Color Space', '', 'scene-linear Rec 709/sRGB'],
['Color Management Preferences', 'Enable Color Managed Pots', '', True],


#---------------------------------------------------------------
Maya Version
pm.versions.current()
# Result: 201507 #
v2015 = 201500
v2015_SP1 = 201501
v2015_SP2 = 201502
v2015_SP3 = 201505
v2015_SP4 = 201506
v2015_EXT1 = 201506
v2015_SP5 = 201507
v2015_EXT1SP5 = 201507
v2016 = 201600
#---------------------------------------------------------------
# Arnold Gamma Correction
setAttr "defaultArnoldRenderOptions.display_gamma" 1;  Display
setAttr "defaultArnoldRenderOptions.light_gamma" 1;     Light
setAttr "defaultArnoldRenderOptions.shader_gamma" 1;    Shaders
setAttr "defaultArnoldRenderOptions.texture_gamma" 1;   Textures

['Arnold Gamma Correction', 'Display Gamma', 'defaultArnoldRenderOptions.display_gamma', 1.0],
['Arnold Gamma Correction', 'Lights Gamma', 'defaultArnoldRenderOptions.light_gamma', 1.0],
['Arnold Gamma Correction', 'Shaders Gamma', 'defaultArnoldRenderOptions.shader_gamma', 1.0],
['Arnold Gamma Correction', 'Textures Gamma', 'defaultArnoldRenderOptions.texture_gamma', 1.0],


# Arnold Render Options

setAttr "defaultArnoldRenderOptions.AASamples" 4;
setAttr "defaultArnoldRenderOptions.GIDiffuseSamples" 3;
setAttr "defaultArnoldRenderOptions.GIGlossySamples" 3;
setAttr "defaultArnoldRenderOptions.GIRefractionSamples" 3;
setAttr "defaultArnoldRenderOptions.sssBssrdfSamples" 4;
['Arnold Samples', 'Camera(AA)', 'defaultArnoldRenderOptions.AASamples', 4.0],
['Arnold Samples', 'Diffuse', 'defaultArnoldRenderOptions.GIDiffuseSamples', 4.0],
['Arnold Samples', 'Glossy', 'defaultArnoldRenderOptions.GIGlossySamples', 4.0],
['Arnold Samples', 'Refraction', 'defaultArnoldRenderOptions.GIRefractionSamples', 4.0],
['Arnold Samples', 'SSS', 'defaultArnoldRenderOptions.sssBssrdfSamples', 4.0],

setAttr "defaultArnoldRenderOptions.GITotalDepth" 1;
setAttr "defaultArnoldRenderOptions.GIDiffuseDepth" 1;
setAttr "defaultArnoldRenderOptions.GIGlossyDepth" 1;
setAttr "defaultArnoldRenderOptions.GIReflectionDepth" 3;
setAttr "defaultArnoldRenderOptions.GIRefractionDepth" 3;
['Arnold Ray Depth', 'Total', 'defaultArnoldRenderOptions.GITotalDepth', 1],
['Arnold Ray Depth', 'Diffuse', 'defaultArnoldRenderOptions.GIDiffuseDepth', 1],
['Arnold Ray Depth', 'Glossy', 'defaultArnoldRenderOptions.GIGlossyDepth', 1],
['Arnold Ray Depth', 'Reflection', 'defaultArnoldRenderOptions.GIReflectionDepth', 1],
['Arnold Ray Depth', 'Refraction', 'defaultArnoldRenderOptions.GIRefractionDepth', 1],


pm.PyNode('defaultArnoldFilter').aiTranslator.set('gaussian')
pm.PyNode('defaultArnoldFilter').width.set(2.0)
['Arnold Filter', 'Type', 'defaultArnoldFilter.aiTranslator', 'gaussian'],
['Arnold Filter', 'Type', 'defaultArnoldFilter.width', 2.0],


setAttr "defaultArnoldRenderOptions.log_to_file" 1;
['Arnold Log', 'Type', 'defaultArnoldRenderOptions.log_to_file', 1],


setAttr "defaultArnoldRenderOptions.textureAutomip" 0;
setAttr "defaultArnoldRenderOptions.textureAcceptUnmipped" 0;
setAttr "defaultArnoldRenderOptions.autotile" 0;
setAttr "defaultArnoldRenderOptions.textureAcceptUntiled" 0;
setAttr "defaultArnoldRenderOptions.use_existing_tiled_textures" 0;
['Arnold Texture', 'Auto-mipmap', 'defaultArnoldRenderOptions.textureAutomip', 0],
['Arnold Texture', 'Accept Unmipped', 'defaultArnoldRenderOptions.textureAcceptUnmipped', 0],
['Arnold Texture', 'Auto-tile', 'defaultArnoldRenderOptions.autotile', 0],
['Arnold Texture', 'Accept Untiled', 'defaultArnoldRenderOptions.textureAcceptUntiled', 0],
['Arnold Texture', 'Use Existing .tx', 'defaultArnoldRenderOptions.use_existing_tiled_textures', 0],

#---------------------------------------------------------------
# Texture File Node
pm.PyNode('file1').colorSpace.get()
# Result: u'scene-linear Rec 709/sRGB' #
#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------
'''