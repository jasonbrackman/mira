# -*- coding: utf-8 -*-
import os
import tempfile
from PySide import QtGui, QtCore
import maya.cmds as mc
import maya.mel as mel

window_name = "Snapshot"


def get_panel():
    current_panel = mc.getPanel(withFocus=1)
    current_panel_type = mc.getPanel(typeOf=current_panel)
    if current_panel_type not in ["model_panel"]:
        return
    return current_panel


def delete_window():
    if mc.window(window_name, exists=1):
        mc.deleteUI(window_name)
    if mc.windowPref(window_name, exists=1):
        mc.windowPref(window_name, remove=1)


def create_panel():
    delete_window()
    mc.window(window_name, title=window_name)
    panel_layout = mc.paneLayout(width=480, height=480)
    model_panel = mc.modelPanel(copy=get_panel() or mc.getPanel(withLabel="Persp View"), menuBarVisible=False)
    mc.showWindow(window_name)
    return model_panel


def set_panel(model_panel):
    mc.modelEditor(model_panel, e=1, displayAppearance="smoothShaded")
    mc.modelEditor(model_panel, edit=True, useDefaultMaterial=False)
    mel.eval('setWireframeOnShadedOption false ' + model_panel)
    mc.modelEditor(model_panel, edit=True, allObjects=False, displayTextures=True)
    mc.modelEditor(model_panel, edit=True, polymeshes=True)
    mc.modelEditor(model_panel, edit=True, pluginObjects=['gpuCacheDisplayFilter', True])
    mc.modelEditor(model_panel, edit=True, grid=False)
    mel.eval('SelectAllPolygonGeometry')
    mel.eval('LowQualityDisplay')
    # mc.viewFit(mc.lookThru(model_panel, query=True), fitFactor=0.8, animate=True)
    mc.select(clear=True)
    mc.modelEditor(model_panel, edit=True, activeView=True)
    mc.setFocus(model_panel)


def playblast_thumb(file_name):
    current_frame = mc.currentTime(q=1)
    path = mc.playblast(format='image', viewer=False, percent=100, quality=100, framePadding=4,
                        width=480, height=480, filename=file_name, endTime=current_frame, startTime=current_frame,
                        offScreen=True, forceOverwrite=True, showOrnaments=False, compression="png")
    delete_window()
    path = path.replace("\\", "/")
    if not path:
        raise RuntimeError('Playblast was canceled')
    src = path.replace("####", str(int(current_frame)).zfill(4))
    return src


def playblast_to_temp():
    model_panel = create_panel()
    set_panel(model_panel)
    temp_dir = tempfile.gettempdir()
    file_name = os.path.join(temp_dir, "playblast").replace("\\", "/")
    return playblast_thumb(file_name)


class Label(QtGui.QLabel):
    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(Label, self).__init__(parent)
        self.file_path = None
        self.clicked.connect(self.set_pixmap)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def set_pixmap(self):
        self.file_path = playblast_to_temp()
        pix_map = QtGui.QPixmap(self.file_path)
        self.setPixmap(pix_map)


def main():
    label = Label()
    return label


if __name__ == "__main__":
    print main()
