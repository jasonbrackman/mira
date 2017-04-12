__author__ = 'heshuai'

import maya.mel as mel
import maya.cmds as mc


def show_outliner_window():
    mel.eval("OutlinerWindow;")


def show_hypershade_window():
    mel.eval("HypershadeWindow;")


def show_reference_editor():
    mel.eval("ReferenceEditor;")


def show_textureview_window():
    mel.eval("TextureViewWindow;")


def show_nodeeditor_window():
    mel.eval("NodeEditorWindow;")


def show_render_view():
    mel.eval('RenderViewWindow;')


def show_render_settings():
    if mc.window('unifiedRenderGlobalsWindow', q=1, exists=1):
        mc.deleteUI('unifiedRenderGlobalsWindow')
    mel.eval('unifiedRenderGlobalsWindow')

