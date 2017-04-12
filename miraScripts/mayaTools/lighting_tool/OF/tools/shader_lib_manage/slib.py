#########################################################################
#
#  SLiB.py
#
#########################################################################


import sys
import os
import imp
import maya.cmds as cmds
import maya.mel as mel

#.WIN.>>>
# Set Path to SLiB Folder here: (use Forward Slash ONLY)

CurrentPath = __file__
SLiBInstallPath = os.path.join(os.path.dirname(CurrentPath), 'SLiB')
SLiBInstallPath = SLiBInstallPath.replace('\\', '/')

#SLiBInstallPath = 'C:/ _INSERT YOUR MAYA PLUGIN PATH HERE_ /SLiB'

#.MAC.>>>
# Set Path to SLiB Folder here:
# SLiBInstallPath = ''


#########################################################################
#########################################################################
#########################################################################

guiPath = SLiBInstallPath + '/' + 'gui' + '/'
imgPath = SLiBInstallPath + '/' + 'img' + '/'
pytPath = SLiBInstallPath + '/' + 'pyt' + '/'
melPath = SLiBInstallPath + '/' + 'mel' + '/'
libPath = SLiBInstallPath + '/' + 'lib' + '/' 
sys.path.append(pytPath)

import SLiBSetupPy
reload(SLiBSetupPy)

def initializePlugin():
    mel.eval('putenv "SLiBGui"      "' + guiPath + '"')
    mel.eval('putenv "SLiBImage"    "' + imgPath + '"')
    mel.eval('putenv "SLiBMel"      "' + melPath + '"')
    mel.eval('putenv "SLiBLib"      "' + libPath + '"')
    reload(SLiBSetupPy)
    SLiBSetupPy.SLiBSetupLoad()
    print '''
            #...........................................................#
            #.:____________[x]========================[x]_____________:.#
            #.:____________:|                          |:_____________:.#
            #.:____________:|   SLiB Plug-In loaded!   |:_____________:.#
            #.:____________:|                          |:_____________:.#
            #              [x]========================[x]               #
            #                                                           #
            #                ShaderLibrary v.01 for Maya                #
            #                                                           #
            #[x]____/"'Oo=-..  (c)opyright by D:G:D:M   ..-=oO'"\____[x]#
        '''

def uninitializePlugin(obj):
    reload(SLiBSetupPy)
    SLiBSetupPy.SLiBSetupUnLoad()
    print "SLiB Plug-In unloaded!"