# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mel


def update_render_setting_window():
    if mc.window('unifiedRenderGlobalsWindow', q=1, exists=1):
        mc.deleteUI('unifiedRenderGlobalsWindow')
    mel.eval('unifiedRenderGlobalsWindow')


if __name__ == "__main__":
    pass
