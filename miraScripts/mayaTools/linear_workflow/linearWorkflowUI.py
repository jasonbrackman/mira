#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename    :
#description :
#author      :Yan-Chen Liao
#date        :2015/5/25
#version     :
#usage       :
#notes       :
#==============================================================================

# Built-in modules
import functools
from decimal import Decimal

# Third-party modules
from PySide import QtCore, QtGui
import pymel.core as pm
import maya.cmds as cmds
from pymel import versions
# Studio modules


class ui(object):
    def __init__(self, parent):
        super(ui, self).__init__()
        self._parent = parent

        # for updating ui and information
        self.grp_dict = dict()      # grp_dict[ groupbox_title ] = qt_QGroupBox
        self.ui_items = dict()      # ( qt_fix_QPushButton, qt_QLabel, qt_ui_item, default_value)
        self.color_management_ui_items = list()
        self.render_option_ui_items = None

        #
        self.lineedit_width = 80
        self.fixbutton_width = 25
        self.label_width = 135


        self.setup_ui()

    # get GroupBox from title
    def getGroupbox(self, title):
        if title not in self.grp_dict.keys():
            groupbox = QtGui.QGroupBox(title)
            groupbox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
            groupbox.setAlignment(QtCore.Qt.AlignTop| QtCore.Qt.AlignVCenter)
            self.grp_dict[title] = groupbox

            groupbox.setLayout(QtGui.QVBoxLayout())
            return groupbox

        else:
            return self.grp_dict[title]

    def groupbox_mayaAttr(self):

        self.mayaAttrList = [
            ['Arnold Samples', 'Camera(AA)', 'defaultArnoldRenderOptions.AASamples', 3],
            ['Arnold Samples', 'Diffuse', 'defaultArnoldRenderOptions.GIDiffuseSamples', 2],
            ['Arnold Samples', 'Glossy', 'defaultArnoldRenderOptions.GIGlossySamples', 2],
            ['Arnold Samples', 'Refraction', 'defaultArnoldRenderOptions.GIRefractionSamples', 1],
            ['Arnold Samples', 'SSS', 'defaultArnoldRenderOptions.GISssSamples', 3],
            ['Arnold Samples', 'Lock Sampleing Pattern', 'defaultArnoldRenderOptions.lock_sampling_noise', True],
            ['Arnold Ray Depth', 'Total', 'defaultArnoldRenderOptions.GITotalDepth', 7],
            ['Arnold Ray Depth', 'Diffuse', 'defaultArnoldRenderOptions.GIDiffuseDepth', 2],
            ['Arnold Ray Depth', 'Glossy', 'defaultArnoldRenderOptions.GIGlossyDepth', 1],
            ['Arnold Ray Depth', 'Reflection', 'defaultArnoldRenderOptions.GIReflectionDepth', 2],
            ['Arnold Ray Depth', 'Refraction', 'defaultArnoldRenderOptions.GIRefractionDepth', 2],
            ['Arnold Gamma Correction', 'Display Gamma', 'defaultArnoldRenderOptions.display_gamma', 1.0],
            ['Arnold Gamma Correction', 'Lights Gamma', 'defaultArnoldRenderOptions.light_gamma', 1.0],
            ['Arnold Gamma Correction', 'Shaders Gamma', 'defaultArnoldRenderOptions.shader_gamma', 1.0],
            ['Arnold Gamma Correction', 'Textures Gamma', 'defaultArnoldRenderOptions.texture_gamma', 1.0],
            ['Arnold Filter', 'Type', 'defaultArnoldFilter.aiTranslator', 'gaussian'],
            ['Arnold Filter', 'Width', 'defaultArnoldFilter.width', 2.0],
            ['Arnold Log', 'Log_to_file', 'defaultArnoldRenderOptions.log_to_file', False],
            ['Arnold Texture', 'Auto-mipmap', 'defaultArnoldRenderOptions.textureAutomip', False],
            ['Arnold Texture', 'Accept Unmipped', 'defaultArnoldRenderOptions.textureAcceptUnmipped', False],
            ['Arnold Texture', 'Auto-tile', 'defaultArnoldRenderOptions.autotile', False],
            ['Arnold Texture', 'Accept Untiled', 'defaultArnoldRenderOptions.textureAcceptUntiled', False],
            ['Arnold Texture', 'Use Existing .tx', 'defaultArnoldRenderOptions.use_existing_tiled_textures', False],
        ]
        for index, item in enumerate(self.mayaAttrList):

            groupbox_title = item[0]
            attr_title = item[1]
            attr_name = item[2]
            attr_default = item[3]

            # groupbox
            groupbox = self.getGroupbox(groupbox_title)
            groupbox_layout = groupbox.layout()

            # item - fix button/attr name/current value
            fix_btn = QtGui.QPushButton('Fix')
            fix_btn.setFixedWidth(self.fixbutton_width)
            attr_label = QtGui.QLabel(attr_title)
            attr_label.setFixedWidth(self.label_width)
            attr_label.setAlignment(QtCore.Qt.AlignRight| QtCore.Qt.AlignVCenter)

            if type(attr_default)==bool:
                attr_ui_item = QtGui.QCheckBox()
            else:
                attr_ui_item = QtGui.QLineEdit()
                attr_ui_item.setFixedWidth(self.lineedit_width)

            # add items to groupbox layout
            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(fix_btn)
            hbox.addWidget(attr_label)
            hbox.addWidget(attr_ui_item)
            groupbox_layout.addLayout(hbox)

            # signal
            fnc_fix = lambda x=attr_name, y=attr_default: self.set_maya_attr(x, y)
            fix_btn.clicked.connect(fnc_fix)

            callback = functools.partial(self.update_maya_attr, attr_ui_item, attr_name)
            if type(attr_default)==bool:
                attr_ui_item.stateChanged.connect(callback)
            else:
                attr_ui_item.editingFinished.connect(callback)

            # dict for updating ui
            self.ui_items[attr_name] = (fix_btn, attr_label, attr_ui_item, attr_default)


        #Add fix all button in each groupbox
        for title in self.grp_dict.keys():
            groupbox = self.getGroupbox(title)
            groupbox_layout = groupbox.layout()
            fixall_btn = QtGui.QPushButton('Fix All - %s'% title)

            callback = functools.partial(self.fix_maya_attr_in_group, title)
            fixall_btn.clicked.connect(callback)
            groupbox_layout.addWidget(fixall_btn)

        #import pprint
        #pprint.pprint(self.ui_items)
        #pprint.pprint(self.grp_dict)

    def fix_maya_attr_in_group(self, group_title):
        for item in self.mayaAttrList:
            if group_title==item[0] or group_title=='all':
                attr_name = item[2]
                attr_default_value = item[3]
                self.set_maya_attr(attr_name, attr_default_value)


    def groupbox_maya_version(self):
        # groupbox
            groupbox = self.getGroupbox('Version')
            groupbox_layout = groupbox.layout()

            is_valid, maya_version = self.mayaVersionString()

            label = QtGui.QLabel(maya_version)
            statusLabel = QtGui.QLabel()
            okIcon = self._parent.style().standardIcon(QtGui.QStyle.SP_DialogApplyButton)
            notOkIcon = self._parent.style().standardIcon(QtGui.QStyle.SP_DialogCancelButton)
            if is_valid:
                label.setStyleSheet('QLabel {font:Bold}')
                statusLabel.setPixmap(okIcon.pixmap(16))
            else:
                label.setStyleSheet('QLabel {font:Bold;color:#FF6600}')
                statusLabel.setPixmap(notOkIcon.pixmap(16))

            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(statusLabel)
            hbox.addWidget(label)
            groupbox_layout.addLayout(hbox)

    def groupbox_render_view_option(self):
        # groupbox
        groupbox = self.getGroupbox('Render View Option')
        groupbox_layout = groupbox.layout()

        # item - fix button/attr name/current value
        fix_btn = QtGui.QPushButton('Fix')
        fix_btn.setFixedWidth(self.fixbutton_width)
        fix_btn.clicked.connect(self.set_render_view_option)
        attr_label = QtGui.QLabel('Save Raw Image')
        attr_label.setFixedWidth(self.label_width)
        attr_label.setAlignment(QtCore.Qt.AlignRight| QtCore.Qt.AlignVCenter)
        attr_ui_item = QtGui.QCheckBox()

        callback = functools.partial(self.set_render_view_option, attr_ui_item)
        attr_ui_item.stateChanged.connect(callback)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(fix_btn)
        hbox.addWidget(attr_label)
        hbox.addWidget(attr_ui_item)
        groupbox_layout.addLayout(hbox)

        self.render_option_ui_items = (fix_btn, attr_label, attr_ui_item)

    def set_render_view_option(self, *args):

        if not args:
            pm.optionVar['renderViewSaveMode'] = 0  # default value: Save Raw Image
        else:
            checkbox = args[0]
            value = checkbox.checkState()
            if value:
                pm.optionVar['renderViewSaveMode'] = 0
            else:
                pm.optionVar['renderViewSaveMode'] = 1

        self.update_render_view_option_ui()

    def update_render_view_option_ui(self):

        if 'renderViewSaveMode' not in pm.optionVar.keys():
            pm.optionVar['renderViewSaveMode'] = 0

        value = pm.optionVar['renderViewSaveMode']
        fix_btn, attr_label, attr_ui_item = self.render_option_ui_items
        if value==0:    # save raw image
            attr_label.setStyleSheet('')
            attr_ui_item.setCheckState(QtCore.Qt.Checked)
            fix_btn.setEnabled(False)
        else:       #save color-managed image
            attr_label.setStyleSheet("QLabel { color : #FF6600;font: Bold }")
            attr_ui_item.setCheckState(QtCore.Qt.Unchecked)
            fix_btn.setEnabled(True)

    def groupbox_color_management(self):
        self.otherAttrList = [
            ['Color Management Preferences', 'Enable', '', True],
            ['Color Management Preferences', 'Rendering Space', '', 'scene-linear Rec 709/sRGB'],
            ['Color Management Preferences', 'View Transform', '', 'sRGB gamma'],
            ['Color Management Preferences', 'Input Color Space', '', 'scene-linear Rec 709/sRGB'],
            ['Color Management Preferences', 'Enable Color Pots', '', True],
        ]
        for index, item in enumerate(self.otherAttrList):
            groupbox_title = item[0]
            attr_title = item[1]
            #attr_name = item[2]
            attr_default = item[3]

            # groupbox
            groupbox = self.getGroupbox(groupbox_title)
            groupbox_layout = groupbox.layout()

            # item - fix button/attr name/current value
            attr_label = QtGui.QLabel(attr_title)
            attr_label.setFixedWidth(self.label_width)
            attr_label.setAlignment(QtCore.Qt.AlignRight| QtCore.Qt.AlignVCenter)

            if type(attr_default)==bool:
                attr_ui_item = QtGui.QCheckBox()
            else:
                attr_ui_item = QtGui.QLineEdit()
                attr_ui_item.setFixedWidth(150)

            # add items to groupbox layout
            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(attr_label)
            hbox.addWidget(attr_ui_item)
            groupbox_layout.addLayout(hbox)

            self.color_management_ui_items.append((attr_label, attr_ui_item, attr_default))

            # command color management not exists
            try:
                cmds.colorManagementPrefs
            except:
                attr_label.setStyleSheet("QLabel { color : #FF6600;font: Bold }")


        groupbox = self.getGroupbox('Color Management Preferences')
        groupbox_layout = groupbox.layout()

        fixall_btn = QtGui.QPushButton('Fix All - Color Management Preferences')
        fixall_btn.clicked.connect(self.set_color_management_attr)

        # colormanagement command not exists
        try:
            cmds.colorManagementPrefs
        except:
            fixall_btn.setEnabled(False)


        groupbox_layout.addWidget(fixall_btn)

    def set_color_management_attr(self):
        #Dont update ui if Color management command not exist
        try:
            cmds.colorManagementPrefs
        except:
            return

        for item in self.otherAttrList:
            #['Color Management Preferences', 'Enable', '', True],
            attr_label = item[1]
            value = item[3]
            if attr_label=='Enable':
                cmds.colorManagementPrefs(e=True, cmEnabled=value)
            elif attr_label=='Rendering Space':
                cmds.colorManagementPrefs(e=True, renderingSpaceName=value)
            elif attr_label=='View Transform':
                cmds.colorManagementPrefs(e=True, viewTransformName=value)
            elif attr_label=='Input Color Space':
                cmds.colorManagementPrefs(e=True, defaultInputSpaceName=value)
            elif attr_label=='Enable Color Pots':
                cmds.colorManagementPrefs(e=True, colorManagePots=value)
        self.update_color_management_ui()

    def update_color_management_ui(self):

        #Dont update ui if Color management command not exist
        try:
            cmds.colorManagementPrefs(q=True, cmEnabled=True)
        except:
            return

        for label, ui_item, default_value in self.color_management_ui_items:
            if label.text()=='Enable':
                value = cmds.colorManagementPrefs(q=True, cmEnabled=True)
            elif label.text()=='Rendering Space':
                value = cmds.colorManagementPrefs(q=True, renderingSpaceName=True)
            elif label.text()=='View Transform':
                value = cmds.colorManagementPrefs(q=True, viewTransformName=True)
            elif label.text()=='Input Color Space':
                value = cmds.colorManagementPrefs(q=True, defaultInputSpaceName=True)
            elif label.text()=='Enable Color Pots':
                value = cmds.colorManagementPrefs(q=True, colorManagePots=True)

            if isinstance(ui_item, QtGui.QLineEdit):
                ui_item.setText(str(value))
                ui_item.setReadOnly(True)
            elif isinstance(ui_item, QtGui.QCheckBox):
                if value:
                    ui_item.setCheckState(QtCore.Qt.Checked)
                else:
                    ui_item.setCheckState(QtCore.Qt.Unchecked)
                ui_item.setEnabled(False)

            if value!=default_value:
                label.setStyleSheet("QLabel { color : #FF6600;font: Bold }")
            else:
                label.setStyleSheet('')


    def setup_ui(self):

        # Generate ui GroupBoxs
        self.groupbox_mayaAttr()
        self.groupbox_color_management()
        self.groupbox_maya_version()
        self.groupbox_render_view_option()

        # Main Vertical Box Layout
        main_vbox = QtGui.QVBoxLayout()


        # Main Layout for groupbox
        groupbox_order = [
            ['Version', 'Color Management Preferences', 'Arnold Gamma Correction'],
            ['Arnold Samples', 'Arnold Ray Depth'],
            ['Arnold Texture', 'Arnold Filter', 'Arnold Log', 'Render View Option']
        ]

        hbox_groupbox = QtGui.QHBoxLayout()
        for title_order in groupbox_order:
            vbox = QtGui.QVBoxLayout()
            for title in title_order:
                groupbox = self.getGroupbox(title)
                vbox.addWidget(groupbox)
            hbox_groupbox.addLayout(vbox)
        main_vbox.addLayout(hbox_groupbox)


        # Fix-all Button
        fixall_btn = QtGui.QPushButton('Fix All')
        callback = functools.partial(self.fix_maya_attr_in_group, 'all')
        fixall_btn.clicked.connect(self.set_default_attr)
        fixall_btn.setFixedHeight(30)
        fixall_btn.setStyleSheet('QPushButton {font:Bold;color:white;background-color:#3DA8B2}')

        main_vbox.addWidget(fixall_btn)
        self._parent.setLayout(main_vbox)

        # update ui content
        self.update_maya_attr_ui()
        self.update_color_management_ui()
        self.update_render_view_option_ui()

    def set_default_attr(self):
        self.fix_maya_attr_in_group('all')
        self.set_color_management_attr()

    #update ui from maya attribute
    def update_maya_attr_ui(self):
        # ui_items
        # ( qt_fix_button, qt_label, qt_ui_item, default_value)

        for attr_name in self.ui_items.keys():
            fix_btn, label, attr_ui_item, attr_default = self.ui_items[attr_name]
            try:
                attr_value = pm.PyNode(attr_name).get()
            except:pass
            if type(attr_value)==float:
                attr_value = round(Decimal(attr_value), 3)

            # current attr_value
            # line_edit
            if isinstance(attr_ui_item, QtGui.QLineEdit):
                attr_ui_item.setText(str(attr_value))
                # validator
                if type(attr_value)==int:
                    attr_ui_item.setValidator(QtGui.QIntValidator())
                elif type(attr_value)==float:
                    attr_ui_item.setValidator(QtGui.QDoubleValidator())

                if type(attr_value)==str or type(attr_value)==unicode:
                    attr_ui_item.setReadOnly(True)
                else:
                    attr_ui_item.setReadOnly(False)

            # checkbox
            elif isinstance(attr_ui_item, QtGui.QCheckBox):
                if attr_value:
                    attr_ui_item.setCheckState(QtCore.Qt.Checked)
                else:
                    attr_ui_item.setCheckState(QtCore.Qt.Unchecked)

            # button enable disable
            if attr_default==attr_value:
                label.setStyleSheet("")
                fix_btn.setEnabled(False)
                fix_btn.setStyleSheet('')
            else:
                label.setStyleSheet("QLabel { color : #FF6600;font: Bold }")
                fix_btn.setEnabled(True)
                fix_btn.setStyleSheet('QPushButton { font:Bold;}')

    # callback for setting maya attribute
    def update_maya_attr(self, *args):
        ui_item = args[0]
        attr_name = args[1]

        value = None
        if isinstance(ui_item, QtGui.QLineEdit):
            try:
                value = float(ui_item.text())
            except:
                value = ui_item.text()
        elif isinstance(ui_item, QtGui.QCheckBox):
            print ui_item.checkState()
            value = bool(ui_item.checkState())

        self.set_maya_attr(attr_name, value)

    # set maya attr
    def set_maya_attr(self, attrname, value):
        print attrname, value
        pm.PyNode(attrname).set(value)
        self.update_maya_attr_ui()

    # get maya version
    def mayaVersionString(self):
        '''
        ver_num = pm.versions.current()
        ver_str = 'Autodesk Maya 2015 Extension 1 + SP5 '

        #2015 Extension 1 + SP5'
        if ver_num==201507:
            return True, ver_str
        else:
            return False, 'Not '+ver_str
        '''
        ver_str = pm.about(iv=1)
        valid_installed_version = 'Autodesk Maya 2015 Extension 1 + SP5'
        if str(valid_installed_version)==ver_str:
            return True, ver_str
        else:
            return False, '%s\n Valid: Autodesk Maya 2015 Extension 1 + SP5' % ver_str