#########################################################################
#
#  SLiBBrowserPy.py v0.1
#
#########################################################################

## > credits for heavy code inspiration to Christian Esbo Agergaard! < ##

import maya.cmds as cmds
import maya.mel as mel
import subprocess
import time
from time import gmtime, strftime
import os
import shutil
import sys
import re
import imp
import fnmatch
import platform
import string
import compiler
SLiBImage = mel.eval('getenv SLiBImage;')


##### SLiB | LOAD TESTROOM #####

def loadTestRoom():

    needSave = cmds.file(q=True, modified=True)
    testroomfile = mel.eval('getenv SLiBLib;') + '/scene/SLiB_ShaderTestRoom_hdri.ma'
    testroomdestination = cmds.workspace(query = True, fullName = True)
    hdrifile = mel.eval('getenv SLiBLib;') + '/scene/TestRoom.hdr'
    bgfile = mel.eval('getenv SLiBLib;') + '/scene/BG_grey.png'
    checkerfile = mel.eval('getenv SLiBLib;') + '/scene/Checker.png'
    
    if needSave:
        cmds.SaveScene()
    else:
        pass
    
    cmds.file( f=True, new=True )
    cmds.file( testroomfile, o=True )
    cmds.setAttr('redshiftDomeLightShape1.tex0', str(hdrifile), type="string")
    cmds.setAttr('redshiftDomeLightShape1.tex1', str(bgfile), type="string")
    cmds.setAttr('RS_CheckerBall_File01.fileTextureName', str(checkerfile), type="string")
    cmds.setAttr('RS_CheckerRoom_File01.fileTextureName', str(checkerfile), type="string")
    t = cmds.date()
    xsplit = t.split('/')
    y = xsplit[-1]
    name = 'RS_Testroom_' + t + '.ma'
    savename1 = name.replace (" ", "_")
    savename2 = savename1.replace ("/", "")
    savename3 = savename2.replace (":", "")
    cmds.file( rename=savename3 )
    cmds.file(save=True, type='mayaAscii' )
    
##### SLiB | BROWSER #####

def SLiBFlushOptionMenu(flushOptionMenu):

    try:
        menuItems = cmds.optionMenu(flushOptionMenu, query = True, itemListLong = True)
        for curItem in menuItems:
            cmds.deleteUI(curItem, menuItem = True)
    except:
        pass

#IMPORT
def SLiBBrowserImport(type):
    selected = cmds.ls(selection = True)
    if cmds.iconTextRadioCollection('slAssetCollection', query = True, select = True) == 'NONE':
        SLiBDialogConfirm('Error while ' + type + '                              ', 'Please select the Shader you want to Import!', 'OK')
        return None

    assetPath = os.path.dirname(cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', query = True, select = True), query = True, label = True))
    importFile = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', query = True, select = True), query = True, label = True)
    fileType = 'mayaAscii'
    aas = cmds.checkBox('SLiBAutoAssign', query = True, value = True)
    before = cmds.ls(materials=1)
    cmds.file(importFile, i = True, type = fileType, usingNamespaces = False, returnNewNodes = True, ignoreVersion = True)
    after  = cmds.ls(materials=1)
    imported = list(set(after)-set(before))
    cmds.scrollField('SLiB_TEXTFIELD_Info', edit = True, text = 'Import %s Successful !!!' % imported[0])
    cmds.select(selected)
    if aas:
        #cmds.sets(selected, e=1, forceElement=shader)
        cmds.hyperShade( a=imported[0])
        

    atf = cmds.checkBox('SLiBAutoTextureFix', query = True, value = True)
    if atf:
        import SLiBFixTexturePathSilentPy
        reload(SLiBFixTexturePathSilentPy)
        SLiBFixTexturePathSilentPy.SLiBFiXiTs()
        
    try:
        cmds.select(selected)
    
    except:
        cmds.iconTextRadioCollection('slAssetCollection', query = True, select = True) == 'NONE'
        cmds.select(clear = True)

        
#UPDATE INFO
def SLiBBrowserUpdateInfo():
    asset = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', query = True, select = True), query = True, annotation = True)
    print asset
    printNotes = 'Shader Name : ' + asset
    printNotes = printNotes + '\n'
    printNotes = printNotes + 'Selected!'
    #printNotes = printNotes + 'Author : ' + str(importNotes['Author']) + ' | Version : ' + str(importNotes['Version']) + ' | Render : ' + str(importNotes['Render'])
    cmds.scrollField('SLiB_TEXTFIELD_Info', edit = True, text = printNotes)
    #assetPath = os.path.dirname(cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', query = True, select = True), query = True, label = True))

#UPDATE SHADER
def SLiBBrowserUpdateShader():
    cmds.optionVar(stringValue = ('SLiBThumbSizeComboBox', cmds.optionMenu('SLiBThumbSizeComboBox', query = True, value = True)))
    cmds.setParent(slBrowserUI)
    cmds.setParent(cmds.button('SLiBIconParenter', query = True, fullPathName = True, parent = True))
    if cmds.scrollLayout('SLiBScrollLayout', query = True, exists = True):
        cmds.deleteUI('SLiBScrollLayout', layout = True)
    
    iconLayout = cmds.optionMenu('SLiBThumbSizeComboBox', query = True, value = True)
    iconSize = iconLayout.split('x')
    if len(iconSize) > 1:
        cmds.scrollLayout('SLiBScrollLayout', childResizable = True)
        if iconLayout == '64x64':
            cmds.rowColumnLayout(numberOfColumns = 12)
        
        if iconLayout == '128x128':
            cmds.rowColumnLayout(numberOfColumns = 6)
        
        if iconLayout == '256x256':
            cmds.rowColumnLayout(numberOfColumns = 3)
        
    else:
        cmds.scrollLayout('SLiBScrollLayout', childResizable = True)
        cmds.rowColumnLayout(numberOfColumns = 2, columnWidth=[(1, 250), (2, 250)])
    assetPath = cmds.optionVar(query = 'SLiBLib') + '/' + cmds.optionMenu('SLiBCategoryComboBox', query = True, value = True) + '/' + cmds.optionMenu('SLiBTypeComboBox', query = True, value = True)
    assetDir = os.listdir(assetPath)
    cmds.optionVar(stringValue = ('SLiBIconCaption', cmds.iconTextCheckBox('SLiBIconCaption', query = True, value = True)))
    if len(assetDir) != 0:
        cmds.iconTextRadioCollection('slAssetCollection')
        for curAsset in assetDir:
            curAssetPath = assetPath + '/' + curAsset + '/'
            if curAsset != '.DS_Store':
                assetFile = os.listdir(curAssetPath)
                for curFile in assetFile:
                    file = os.path.splitext(curFile)[0]
                    fileEx = os.path.splitext(curFile)[1]
                    if fileEx == '.mb' or fileEx == '.ma':
                        image = curAssetPath + file + '.png'
                        if not os.path.isfile(image):
                            image = curAssetPath + file + '.ma.swatch'
                        if not os.path.isfile(image):
                            image = curAssetPath + file + '.mb.swatch'
                        if len(iconSize) > 1:
                            if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
                               cmds.columnLayout(rowSpacing = 6, columnWidth = int(iconSize[0]))
                            assetIcon = cmds.iconTextRadioButton(image1 = image, height = int(iconSize[0]), width = int(iconSize[0]), onCommand = 'SLiBBrowserPy.SLiBBrowserUpdateInfo()', label = curAssetPath + curFile, annotation = file)
                            if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
                                cmds.text(label = file, width = int(iconSize[0]), align = 'left')
                                cmds.setParent('..')
                            
                        else:
                            cmds.rowColumnLayout(numberOfColumns = 3, columnWidth = [
                                (1, 64),
                                (2, 8),
                                (3, 435)])
                            #assetIcon = cmds.iconTextRadioButton(image1 = image, height = 64, width = 32, label = curAssetPath + curFile, annotation = file)
                            assetIcon = cmds.iconTextRadioButton(image1 = image, height = 64, width = 32, onCommand = 'SLiBBrowserPy.SLiBBrowserUpdateInfo()', label = curAssetPath + curFile, annotation = file)
                            cmds.text(label = '')
                            cmds.text(label = file, align = 'left')
                            cmds.setParent('..')
                    len(iconSize) > 1
                
        
    
    cmds.optionVar(stringValue = ('SLiBCategoryComboBox', cmds.optionMenu('SLiBCategoryComboBox', query = True, value = True)))
    cmds.optionVar(stringValue = ('SLiBTypeComboBox', cmds.optionMenu('SLiBTypeComboBox', query = True, value = True)))

#UPDATE TYPE
def SLiBBrowserUpdateType():
    SLiBFlushOptionMenu('SLiBTypeComboBox')
    
    typeList = os.listdir(cmds.optionVar(query = 'SLiBLib') + '/' + cmds.optionMenu('SLiBCategoryComboBox', query = True, value = True))

    if len(typeList) != 0:
        cmds.optionMenu('SLiBTypeComboBox', edit = True, enable = True)
        cmds.setParent('SLiBTypeComboBox', menu = True)
        for curType in typeList:
            if curType != '.DS_Store':
                cmds.menuItem(label = curType)
                continue
        
        
        try:
            cmds.optionMenu('SLiBTypeComboBox', edit = True, value = cmds.optionVar(query = 'SLiBTypeComboBox'))
        except:
            pass

        SLiBBrowserUpdateShader()
    else:
        cmds.optionMenu('SLiBTypeComboBox', edit = True, enable = False)
        if cmds.scrollLayout('SLiBScrollLayout', query = True, exists = True):
            cmds.deleteUI('SLiBScrollLayout', layout = True)
        
#UPDATE BROWSER
def SLiBBrowserUpdate():
    SLiBFlushOptionMenu('SLiBCategoryComboBox')
    cateList = os.listdir(cmds.optionVar(query = 'SLiBLib'))
    if len(cateList) != 0:
        cmds.optionMenu('SLiBCategoryComboBox', edit = True, enable = True)
        cmds.setParent('SLiBCategoryComboBox', menu = True)
        for curCate in cateList:
            if curCate != '.DS_Store':
                cmds.menuItem(label = curCate)
                continue
        
        
        try:
            cmds.optionMenu('SLiBCategoryComboBox', edit = True, value = cmds.optionVar(query = 'SLiBCategoryComboBox'))
        except:
            pass

        SLiBBrowserUpdateType()
    else:
        cmds.optionMenu('SLiBCategoryComboBox', edit = True, enable = False)
        cmds.optionMenu('SLiBTypeComboBox', edit = True, enable = False)

#BROWSER DOCKED
def SLiBBrowserDockedUI():
    if cmds.dockControl('slBrowserDock', query = True, exists = True):
        cmds.deleteUI('slBrowserDock')
    
    SLiBBrowserUI()
    mainWindow = cmds.paneLayout(parent = mel.eval('$temp1=$gMainWindow'))
    cmds.dockControl('slBrowserDock', width = 275, area = 'right', label = 'SLiB Browser', content = mainWindow, allowedArea = [
        'right',
        'left'], backgroundColor = [
        4.6007e+18,
        4.6007e+18,
        4.6007e+18])
    cmds.control(slBrowserUI, edit = True, parent = mainWindow)

#BROWSER UI
def SLiBBrowserUI():
    global slBrowserUI
    if cmds.optionVar(query = 'SLiBLib') == 'NoPath':
        SLiBDialogConfirm('Error', 'SLiB Library path not set.\nCheck Settings...', 'OK')
        return None
    SLiBGuiPath = mel.eval('getenv SLiBGui;')
    SLiBImage = mel.eval('getenv SLiBImage;')
    
    try:
        if cmds.window(slBrowserUI, query = True, exists = True):
            cmds.deleteUI(slBrowserUI)
        
        slBrowserUI = cmds.loadUI(uiFile = SLiBGuiPath + 'SLiBBrowser.ui')
    except:
        cmds.optionVar(query = 'SLiBLib') == 'NoPath'
        slBrowserUI = cmds.loadUI(uiFile = SLiBGuiPath + 'SLiBBrowser.ui')

    if cmds.dockControl('slBrowserDock', query = True, exists = True):
        cmds.deleteUI('slBrowserDock')
    
    
    try:
        cmds.optionMenu('SLiBThumbSizeComboBox', edit = True, value = cmds.optionVar(query = 'SLiBThumbSizeComboBox'))
    except:
        cmds.optionVar(query = 'SLiBLib') == 'NoPath'

    cmds.setParent(cmds.button('SLiB_BUTTON_Caption', query = True, fullPathName = True, parent = True))
    cmds.deleteUI('SLiB_BUTTON_Caption')
    cmds.iconTextCheckBox('SLiBIconCaption', image = SLiBImage + 'SLiB_ic_off.png', selectionImage = SLiBImage + 'SLiB_ic_on.png', changeCommand = 'SLiBBrowserPy.SLiBBrowserUpdateShader()')
    cmds.setParent(slBrowserUI)
    if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
        cmds.iconTextCheckBox('SLiBIconCaption', edit = True, value = True)
    
    cmds.showWindow(slBrowserUI)
    if platform.system() == 'Windows':
        cmds.window(slBrowserUI, edit = True, topEdge = True, maximizeButton = False)
    
    cmds.optionMenu('SLiBThumbSizeComboBox', edit = True, changeCommand = 'SLiBBrowserPy.SLiBBrowserUpdateShader()')
    cmds.optionMenu('SLiBCategoryComboBox', edit = True, changeCommand = 'SLiBBrowserPy.SLiBBrowserUpdateType()')
    cmds.optionMenu('SLiBTypeComboBox', edit = True, changeCommand = 'SLiBBrowserPy.SLiBBrowserUpdateShader()')
    SLiBBrowserUpdate()
    
    try:
        cmds.deleteUI('slBrowserDock')
    except:
        cmds.optionVar(query = 'SLiBLib') == 'NoPath'


##### SLiB | SETTINGS #####

#SAVE
def SLiBSetupSettingsSave():
    SLiBLib = cmds.textField('SLiBLibLineEdit', query = True, text = True)
    if SLiBLib != cmds.optionVar(query = 'SLiBLib'):
        if not os.path.exists(SLiBLib):
            SLiBDialogConfirm('SLiB Library Path not found?!.', 'OK')
            return None
        cmds.optionVar(stringValue = ('SLiBLib', SLiBLib.replace('\\', '/')))

    SLiBSetupSettingssUIClose()

#SETUP UI
def SLiBSetupSettingsUI():
    global SLiBSettingsUI
    SLiBGuiPath = mel.eval('getenv SLiBGui;')
    
    try:
        if cmds.window(SLiBSettingsUI, exists = True):
            cmds.deleteUI(SLiBSettingsUI)
        
        SLiBSettingsUI = cmds.loadUI(uiFile = SLiBGuiPath + 'SLiBSettings.ui')
    except:
        SLiBSettingsUI = cmds.loadUI(uiFile = SLiBGuiPath + 'SLiBSettings.ui')

    if platform.system() == 'Windows':
        cmds.textField('SLiBLibLineEdit', edit = True, text = cmds.optionVar(query = 'SLiBLib'))
    else:
        cmds.textField('SLiBLibLineEdit', edit = True, text = cmds.optionVar(query = 'SLiBLib'))

    cmds.showWindow(SLiBSettingsUI)
    if platform.system() == 'Windows':
        cmds.window(SLiBSettingsUI, edit = True, titleBar = True, topEdge = True)
    
#PATH BUTTON
def SLiBSetupPathButton():
    filePath = cmds.fileDialog2(startingDirectory = os.sep, fileMode = 3)
    
    try:
        if platform.system() == 'Windows':
            exportPathEdit = cmds.textField('SLiBLibLineEdit', edit = True, text = filePath[0].replace('/', '\\'))
        else:
            exportPathEdit = cmds.textField('SLiBLibLineEdit', edit = True, text = filePath[0])
    except:
        pass

#CLOSE
def SLiBSetupSettingssUIClose():
    cmds.deleteUI(SLiBSettingsUI)


##### DIALOG #####

def SLiBDialogFileOpen(startingDirectory, fileMode, fileFilter):
    file = cmds.fileDialog2(startingDirectory = startingDirectory, fileMode = fileMode, fileFilter = fileFilter)
    return file

def SLiBDialogPromptYesNo(title, message, yes, no):
    result = cmds.confirmDialog(title = title, message = message, button = [
        yes,
        no], defaultButton = yes, cancelButton = no, dismissString = no)
    return result

def SLiBDialogPromptYesNoCancel(title, message, yes, no, cancel):
    result = cmds.confirmDialog(title = title, message = message, button = [
        yes,
        no,
        cancel], defaultButton = yes, cancelButton = cancel, dismissString = cancel)
    return result

def SLiBDialogConfirm(title, message, confirm):
    cmds.confirmDialog(title = title, message = message, button = confirm)

def SLiBDialogPromptVariable(title, message, text):
    result = cmds.promptDialog(title = title, message = message, text = text, button = [
        'OK',
        'Cancel'], defaultButton = 'OK', cancelButton = 'Cancel', dismissString = 'Cancel')
    if result == 'OK':
        text = cmds.promptDialog(query = True, text = True)
        if text == '':
            SLiBDialogConfirm('Error', 'Needs a name!', 'OK')
        else:
            return text
    text == ''

def SLiBDialogPromptVariableAndStayOpen(title, message, text, ok, close):
    result = cmds.promptDialog(title = title, message = message, text = text, button = [
        ok,
        close], defaultButton = ok, cancelButton = close, dismissString = close)
    if result != close:
        return cmds.promptDialog(query = True, text = True)
    return 0
    
