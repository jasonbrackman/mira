# -*- coding: utf-8 -*-
import maya.mel as mel


def close_panel_open_and_save():
    mel.eval("$gUseSaveScenePanelConfig = false;file -uc false;")
    mel.eval("$gUseSaveScenePanelConfig = false;file -uc false;")
