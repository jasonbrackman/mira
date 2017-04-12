__author__ = 'heshuai'


import maya.mel as mel


def fix_renderlayer_error():
    mel.eval("fixRenderLayerOutAdjustmentErrors;")