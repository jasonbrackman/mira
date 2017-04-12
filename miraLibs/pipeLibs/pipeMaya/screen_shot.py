# -*- coding: utf-8 -*-
import os
import maya.mel as mel
import maya.cmds as cmds


class ScreenShot(object):

    def __init__(self, file_name, sceneSnap=False):
        self.__file = file_name
        self.__sceneSnap = sceneSnap

    def screen_shot(self,):
        cmds.displayPref(displayGradient=1)
        Dir = os.path.dirname(self.__file)
        if not os.path.exists(Dir):
            os.makedirs(Dir)
        self.__file = self.__file.split('.')[0]
        WindowName = 'Snapshot'
        if cmds.window(WindowName, exists=True):
            cmds.deleteUI(WindowName, window=True)
        if cmds.windowPref(WindowName, exists=True):
            cmds.windowPref(WindowName, remove=True)
        cmds.window(WindowName, title='Snapshot')
        modelPanels = cmds.getPanel(typ="modelPanel")
        for currentPanel in modelPanels:
            cmds.modelEditor(currentPanel, e=True, displayAppearance='smoothShaded')
        PaneLayout = cmds.paneLayout(width=480, height=480)
        if self.__sceneSnap:
            ModelPanel = cmds.modelPanel(copy=cmds.getPanel(withLabel='Persp View'), menuBarVisible=False)
            cmds.camera('persp', e=1, displayFilmGate=False, displayResolution=False)
            cmds.setAttr('persp.rx', -45)
            cmds.setAttr('persp.ry', 45)
        else:
            ModelPanel = cmds.modelPanel(copy=cmds.getPanel(withLabel='Front View'), menuBarVisible=False)
            cmds.camera('front', e=1, displayFilmGate=False, displayResolution=False)
        cmds.showWindow(WindowName)
        cmds.modelEditor(ModelPanel, edit=True, useDefaultMaterial=False)
        mel.eval('setWireframeOnShadedOption false ' + ModelPanel)
        cmds.modelEditor(ModelPanel, edit=True, allObjects=False, displayTextures=True)
        cmds.modelEditor(ModelPanel, edit=True, polymeshes=True)
        cmds.modelEditor(ModelPanel, edit=True, pluginObjects=['gpuCacheDisplayFilter', True])
        cmds.modelEditor(ModelPanel, edit=True, grid=False)
        mel.eval('SelectAllPolygonGeometry')
        mel.eval('LowQualityDisplay')
        cmds.viewFit(cmds.lookThru(ModelPanel, query=True), fitFactor=0.8, animate=True)
        cmds.select(clear=True)
        cmds.modelEditor(ModelPanel, edit=True, activeView=True)
        cmds.playblast(
            startTime=0,
            endTime=0,
            format='image',
            filename=self.__file,
            sequenceTime=False,
            clearCache=True,
            viewer=False,
            showOrnaments=False,
            offScreen=True,
            framePadding=4,
            percent=100,
            compression='png',
            quality=100,
            widthHeight=[480, 480])
        if cmds.window(WindowName, exists=True):
            cmds.deleteUI(WindowName, window=True)
        if cmds.windowPref(WindowName, exists=True):
            cmds.windowPref(WindowName, remove=True)
        if os.path.exists(self.__file + '.png'):
            os.remove(self.__file + '.png')
        os.rename(self.__file + '.0000.png', self.__file + '.png')


if __name__ == '__main__':
    ScreenShot('c:/kk.png').screen_shot()
