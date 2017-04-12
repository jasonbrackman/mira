__author__ = 'heshuai'

import maya.mel as mel


def hide_UI_elements():
    mel.eval('''shelfVisibilityStateChange(`toolBar -e -visible 0 MayaWindow|toolBar2`, "");
            statusLineVisibilityStateChange(`toolBar -e -visible  0 MayaWindow|toolBar1`, "");
            toolboxVisibilityStateChange(`toolBar -e -visible 0 MayaWindow|toolBar7`, "");''')


def show_UI_elements():
    mel.eval('RestoreUIElements;')
