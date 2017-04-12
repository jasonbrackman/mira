#########################################################################
#
#  SLiBCopyTexSetPathPy.py v0.1
#
#########################################################################


import maya.cmds as cmds
import maya.mel as mel
import maya.cmds as mc
import os
import time
import shutil

def copyTexturesToProject(object):
    texlistN = cmds.ls(type='RedshiftNormalMap')
    texlist = cmds.ls(type='file')
    textdestination = cmds.workspace(query = True, fullName = True) + "/" + 'sourceimages'
    textdestinationN = cmds.workspace(query = True, fullName = True) + "/" + 'sourceimages'
    si = 'sourceimages'
    window = cmds.window( title="SLiB | INFO:", iconName='Short Name', widthHeight=(400, 330), mxb=False, s=False )
    mc.columnLayout()
    progressControl = mc.progressBar(maxValue=100, width=400, height=40)
    cmds.cmdScrollFieldReporter(width=400, height=258, clear=True)
    cmds.button( label='CLOSE', width=400, height=30, command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    cmds.setParent( '..' )
    cmds.showWindow( window )

    for i in texlist:
        fileName = cmds.getAttr("%s.fileTextureName" %i)
        finalName = fileName.split("/")[-1]
        finalPath = textdestination + "/" + finalName 
        if si in fileName:
            pass
        
        else:            
            shutil.copy(fileName, textdestination)
            cmds.setAttr("%s.fileTextureName" %i, finalPath, type="string")
            print 'copying: >>>' + '  ' + i

    for n in texlistN:
        fileNameN = cmds.getAttr("%s.tex0" %n)
        finalNameN = fileNameN.split("/")[-1]
        finalPathN = textdestination + "/" + finalNameN
        if si in fileNameN:
            pass
        
        else:            
            shutil.copy(fileNameN, textdestinationN)
            cmds.setAttr("%s.tex0" %n, finalPathN, type="string")
            print 'copying: >>>' + '  ' + n

    for r in range(0,100):
        progressInc = mc.progressBar(progressControl, edit=True, pr=r+1)
        time.sleep(0.02)

    print '\nDONE! \n\nNew Texture Path set to:\n\n' + textdestination

#copyTexturesToProject(object)