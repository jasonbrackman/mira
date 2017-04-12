#########################################################################
#
#  SLiBSetupPy.py v0.1
#
#########################################################################


import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import string
import compiler
import platform
import time

def SLiBSetupMenu():
    gMainWindow = mel.eval('$temp1=$gMainWindow')
    if cmds.menu('SLiBMenu', query = True, exists = True):
        cmds.deleteUI('SLiBMenu', menu = True)
    SLiBMenu = cmds.menu('SLiBMenu', parent = gMainWindow, tearOff = True, label = 'SLiB')
    cmds.menuItem(parent = 'SLiBMenu', label = 'Settings', command = 'import SLiBBrowserPy;reload(SLiBBrowserPy);SLiBBrowserPy.SLiBSetupSettingsUI()')
    cmds.menuItem(parent = 'SLiBMenu', divider=True)    
    cmds.menuItem(parent = 'SLiBMenu', label = 'SLiB Browser ...', command = 'import SLiBBrowserPy;reload(SLiBBrowserPy);SLiBBrowserPy.SLiBBrowserUI()')
    cmds.menuItem(parent = 'SLiBMenu', divider=True)
    cmds.menuItem(parent = 'SLiBMenu', label = 'Homepage', command = 'import maya;maya.cmds.showHelp("http://www.slib.digidim.info", absolute=True)')


def SLiBSetupMenuRemove():
    if cmds.menu('SLiBMenu', query = True, exists = True):
        cmds.deleteUI('SLiBMenu', menu = True)
 
def SLiBSetupLoad():
    try:
        SLiBSetupUnLoad()
    except:pass
    SLiBSetupMenu()

def SLiBSetupUnLoad():
    SLiBSetupMenuRemove()
    