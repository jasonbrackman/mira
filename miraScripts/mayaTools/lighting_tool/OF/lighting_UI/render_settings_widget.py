__author__ = 'heshuai'
# -*- coding=UTF-8 -*-

from PySide import QtGui, QtCore
import maya_ctrls
reload(maya_ctrls)
from maya_ctrls import get_os_type
import maya.cmds as mc
import maya.mel as mel
import public_ctrls
import public_ctrls.cpickle_operation as cpickle_operation
import public_ctrls.json_operation as json_operation
import public_ctrls.warm_tip as warm_tip
import os
from get_parent_dir import get_parent_dir



class RenderSettingsWidget(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(RenderSettingsWidget, self).__init__(parent)
        self.setWindowTitle('Render Settings')
        ########
        self.parent_dir = get_parent_dir()
        self.os_type = get_os_type.get_os_type()
        main_widget = QtGui.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtGui.QHBoxLayout(main_widget)
        frame = QtGui.QFrame()
        frame.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Sunken)
        main_layout.addWidget(frame)
        render_settings_layout = QtGui.QVBoxLayout(frame)
        render_settings_grp = QtGui.QGroupBox('Render Settings')
        render_settings_grp.setStyleSheet("QGroupBox{color:#32CD32;border: 1px solid #A9A9A9;"
                                          "padding-top:15px;border-radius:2px;font-size: 15px}")
        render_settings_layout.addWidget(render_settings_grp)
        render_setting_layout = QtGui.QVBoxLayout(render_settings_grp)
        aov_grp = QtGui.QGroupBox('AOV')
        aov_grp.setStyleSheet("QGroupBox{color:#32CD32;border: 1px solid #A9A9A9;"
                              "padding-top:15px;border-radius:2px;font-size: 15px}")
        render_settings_layout.addWidget(aov_grp)
        ########project layout
        project_layout = QtGui.QHBoxLayout()
        project_label = QtGui.QLabel('Project:')
        project_label.setFixedWidth(40)
        self.project_cbox = QtGui.QComboBox()
        self.project_check_btn = QtGui.QPushButton('check')
        self.project_check_btn.setFixedWidth(40)
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)
        project_layout.addWidget(self.project_check_btn)
        ########args layout
        args_layout = QtGui.QHBoxLayout()
        frame_range_label = QtGui.QLabel('Frame Range')
        frame_range_label.setFixedWidth(100)
        self.first_frame_line = QtGui.QLineEdit()
        self.last_frame_line = QtGui.QLineEdit()
        args_layout.addWidget(frame_range_label)
        args_layout.addWidget(self.first_frame_line)
        args_layout.addWidget(self.last_frame_line)
        ########camera layout
        cam_layout = QtGui.QHBoxLayout()
        cam_label = QtGui.QLabel('Render Camera')
        cam_label.setFixedWidth(100)
        self.cam_cbox = QtGui.QComboBox()
        self.cam_cbox.setFixedWidth(240)
        cam_layout.addWidget(cam_label)
        cam_layout.addWidget(self.cam_cbox)
        ########render setting button layout
        render_settings_btn_layout = QtGui.QHBoxLayout()
        self.test_render_btn = QtGui.QPushButton('Test Render Settings')
        self.final_render_btn = QtGui.QPushButton('Final Render Settings')
        render_settings_btn_layout.addWidget(self.test_render_btn)
        render_settings_btn_layout.addWidget(self.final_render_btn)
        ########aov_status_layout
        aov_status_layout = QtGui.QHBoxLayout(aov_grp)
        self.enable_aov_btn = QtGui.QPushButton('Enable AOVs')
        self.disable_aov_btn = QtGui.QPushButton('Disable AOVs')
        self.remove_layer_override_btn = QtGui.QPushButton('Remove Layer Override')
        aov_status_layout.addWidget(self.remove_layer_override_btn)
        aov_status_layout.addWidget(self.enable_aov_btn)
        aov_status_layout.addWidget(self.disable_aov_btn)
        ########mask layer override button
        self.mask_setting_btn = QtGui.QPushButton('Mask Layer Override')
        ########total layout
        render_setting_layout.addLayout(project_layout)
        render_setting_layout.addLayout(args_layout)
        render_setting_layout.addLayout(cam_layout)
        render_setting_layout.addLayout(render_settings_btn_layout)
        #render_settings_layout.addLayout(aov_status_layout)
        render_settings_layout.addWidget(self.mask_setting_btn)
        self.create_action()
        self.create_menu_bar()
        self.create_status_bar()
        self.init_settings()
        self.set_signals()

    def create_action(self):
        self.new_project_action = QtGui.QAction('New Project', self)
        self.remove_project_menu = QtGui.QMenu('Remove Project', self)

    def create_menu_bar(self):
        menu_bar = QtGui.QMenuBar()
        self.setMenuBar(menu_bar)
        project_menu_bar = menu_bar.addMenu('project')
        project_menu_bar.addAction(self.new_project_action)
        project_menu_bar.addMenu(self.remove_project_menu)

    def create_status_bar(self):
        self.status_bar = QtGui.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Welcome to use...')

    def init_settings(self):
        ########project
        self.update_project()
        self.read_setting()
        self.set_project_init_settings()
        ########frames
        self.first_frame_line.setText(str(maya_ctrls.get_first_frame()))
        self.last_frame_line.setText(str(maya_ctrls.get_last_frame()))
        ########cameras
        model = QtGui.QStandardItemModel(self.cam_cbox)
        cameras = mc.ls(type='camera')
        for cam in cameras:
            item = QtGui.QStandardItem(cam)
            model.appendRow(item)
        self.cam_cbox.setModel(model)
        for cam in cameras:
            if mc.getAttr('%s.renderable' % cam):
                if cam not in ['frontShape', 'perspShape', 'sideShape', 'topShape']:
                    self.cam_cbox.setCurrentIndex(self.cam_cbox.findText(cam))
                else:
                    self.cam_cbox.setCurrentIndex(self.cam_cbox.count()+1)

    def set_signals(self):
        self.new_project_action.triggered.connect(self.create_new_project)
        self.test_render_btn.clicked.connect(self.test_settings)
        self.final_render_btn.clicked.connect(self.final_settings)
        self.remove_layer_override_btn.clicked.connect(self.remove_layer_override)
        self.enable_aov_btn.clicked.connect(self.enable_AOVs)
        self.disable_aov_btn.clicked.connect(self.disable_AOVs)
        self.mask_setting_btn.clicked.connect(self.mask_layer_override)
        self.project_cbox.currentIndexChanged.connect(self.set_project_init_settings)
        self.project_check_btn.clicked.connect(self.check_attributes)

    def update_project(self):
        self.remove_project_menu.clear()
        self.project_cbox.clear()
        project_ini_path = os.path.join(self.parent_dir, 'ini', 'project.data')
        if os.path.isfile(project_ini_path):
            project_names = cpickle_operation.get_cpickle_data(project_ini_path)
            if project_names:
                for project_name in project_names:
                    self.project_cbox.addItem(project_name)
                    self.project_action = QtGui.QAction(project_name, self)
                    self.project_action.triggered.connect(self.remove_project)
                    self.remove_project_menu.addAction(self.project_action)
                self.project_cbox.setCurrentIndex(self.project_cbox.count()+1)

    def create_new_project(self):
        global project_widget
        try:
            project_widget.close()
            project_widget.deleteLater()
        except:pass
        project_widget = ProjectWidget(public_ctrls.get_maya_win())
        project_widget.show()

    def set_project_init_settings(self):
        self.status_bar.showMessage('Current Project:  %s' % self.project_cbox.currentText())

    def remove_project(self):
        project_ini_path = os.path.join(self.parent_dir, 'ini', 'project.data')
        project_names = cpickle_operation.get_cpickle_data(project_ini_path)
        project_names.remove(self.sender().text())
        cpickle_operation.set_cpickle_data(project_ini_path, project_names)
        self.sender().deleteLater()
        self.update_project()

    def check_attributes(self):
        project_name = self.project_cbox.currentText()
        if project_name:
            self.create_new_project()
            try:
                project_widget.project_name_cbox.setCurrentIndex(project_widget.project_name_cbox.findText(project_name))
            except:pass
                
    def write_setting(self):
        if self.os_type == 'windows':
            latest_project_data_path = os.path.join(os.environ['APPDATA'], 'latest_project.data')
        if self.os_type == 'linux':
            latest_project_data_path = os.path.join('/tmp', 'latest_project.data')
        cpickle_operation.set_cpickle_data(latest_project_data_path, self.project_cbox.currentText())

    def read_setting(self):
        if self.os_type == 'windows':
            latest_project_data_path = os.path.join(os.environ['APPDATA'], 'latest_project.data')
        if self.os_type == 'linux':
            latest_project_data_path = os.path.join('/tmp', 'latest_project.data')
        if os.path.isfile(latest_project_data_path):
            value = cpickle_operation.get_cpickle_data(latest_project_data_path)
            if self.project_cbox.findText(value) != -1:
                self.project_cbox.setCurrentIndex(self.project_cbox.findText(value))

    def closeEvent(self, event):
        self.write_setting()

    def common_settings(self):
        if not mc.pluginInfo('mtoa.mll', q=1, loaded=1):
            mc.loadPlugin('mtoa.mll')
        mc.setAttr('defaultRenderGlobals.currentRenderer', 'arnold', type='string')
        mel.eval('unifiedRenderGlobalsWindow')
        if self.cam_cbox.currentText():
            if self.project_cbox.currentText():
                current_render_settings_path = os.path.join(self.parent_dir, 'data', 'render_settings_data')
                current_render_settings_path = os.path.join(current_render_settings_path, '%s_render_settings.json' % self.project_cbox.currentText())
                attr_data = json_operation.get_json_data(current_render_settings_path)
                for attr in attr_data:
                    if attr_data[attr]:
                        try:
                            maya_ctrls.set_attr(attr, int(attr_data[attr]))
                        except:
                            maya_ctrls.set_attr(attr, float(attr_data[attr]))
                start = int(float(self.first_frame_line.text()))
                end = int(float(self.last_frame_line.text()))
                render_camera = self.cam_cbox.currentText()
                mc.setAttr('defaultRenderGlobals.currentRenderer', 'arnold', type='string')
                mc.setAttr('defaultRenderGlobals.imageFilePrefix', '<RenderLayer>/<RenderLayer>', type='string')
                #mc.setAttr('defaultRenderGlobals.imfPluginKey', 'exr', type='string')
                #mc.setAttr('defaultRenderGlobals.imageFormat',51)
                mc.setAttr("defaultArnoldDriver.aiTranslator", 'exr', type='string')
                mc.setAttr('defaultArnoldDriver.exrCompression', 2)
                mc.setAttr('defaultArnoldDriver.halfPrecision', 1)
                mc.setAttr('defaultRenderGlobals.animation', 1)
                mc.setAttr('defaultRenderGlobals.periodInExt', 1)
                mc.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
                mc.setAttr('defaultRenderGlobals.extensionPadding', 4)
                mc.setAttr('defaultRenderGlobals.startFrame', start)
                mc.setAttr('defaultRenderGlobals.endFrame', end)
                mc.setAttr('defaultArnoldRenderOptions.abortOnError', 0)
                maya_ctrls.set_render_camera(render_camera)
                #maya_ctrls.rebuild_arnold_aov()
                maya_ctrls.add_aov('N')
                maya_ctrls.add_aov('Z')
                maya_ctrls.add_aov('P')
                maya_ctrls.add_aov('beauty')
                maya_ctrls.add_aov('direct_diffuse')
                maya_ctrls.add_aov('direct_specular')
                maya_ctrls.add_aov('indirect_diffuse')
                maya_ctrls.add_aov('specular')
                maya_ctrls.add_aov('sss')
                maya_ctrls.add_aov('indirect_specular')
                maya_ctrls.add_aov('reflection')
                maya_ctrls.add_aov('refraction')
                mc.setAttr('defaultArnoldDriver.mergeAOVs', 1)
            else:
                self.warm_tip('Please select a project')
        else:
            self.warm_tip('Please select a camera')             
        
    def test_settings(self):
        self.common_settings()
        mc.setAttr('defaultArnoldRenderOptions.AASamples', 2)
        mc.setAttr('defaultArnoldRenderOptions.GIDiffuseSamples', 1)
        mc.setAttr('defaultArnoldRenderOptions.GIGlossySamples', 1)
        mc.setAttr('defaultArnoldRenderOptions.GIRefractionSamples', 1)
        mc.setAttr('defaultArnoldRenderOptions.sssBssrdfSamples', 1)
        try:
            mc.setAttr('defaultArnoldRenderOptions.volumeIndirectSamples', 0)
        except:pass
        mc.setAttr('defaultArnoldRenderOptions.GIDiffuseDepth', 1)
        mc.setAttr('defaultArnoldRenderOptions.GIGlossyDepth', 1)
        mc.setAttr('defaultArnoldRenderOptions.GIReflectionDepth', 2)
        mc.setAttr('defaultArnoldRenderOptions.GIRefractionDepth', 2)
        mc.setAttr('defaultArnoldRenderOptions.motion_blur_enable', 0)
        mc.setAttr('defaultArnoldRenderOptions.ignoreSubdivision', 1)
        mc.setAttr('defaultArnoldRenderOptions.ignoreDisplacement', 1)
        mc.setAttr('defaultArnoldRenderOptions.ignoreBump', 1)
        maya_ctrls.set_aov_enabled(0)
        
    def final_settings(self):
        self.common_settings()
        mc.setAttr('defaultArnoldRenderOptions.motion_blur_enable', 1)
        mc.setAttr('defaultArnoldDriver.halfPrecision', 0)
        mc.setAttr('defaultArnoldRenderOptions.ignoreSubdivision', 0)
        mc.setAttr('defaultArnoldRenderOptions.ignoreDisplacement', 0)
        mc.setAttr('defaultArnoldRenderOptions.ignoreBump', 0)
        maya_ctrls.set_aov_enabled(1) 

    def mask_layer_override(self):
        current_layer = mc.editRenderLayerGlobals(currentRenderLayer=1, q=1)
        if mc.getAttr('defaultRenderGlobals.currentRenderer') == 'arnold':
            if current_layer != 'defaultRenderLayer':
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.GIDiffuseSamples', 0)
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.GIGlossySamples', 0)
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.GIRefractionSamples', 0)
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.sssBssrdfSamples', 0)
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.volumeIndirectSamples', 0)
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.GIDiffuseDepth', 0)
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.GIGlossyDepth', 0)
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.GIReflectionDepth', 0)
                maya_ctrls.set_layer_override('defaultArnoldRenderOptions.GIRefractionDepth', 0)
            else:
                self.warm_tip("Make sure current layer is not masterLayer")
        else:
            self.warm_tip("Current renderer is not arnold")

    def remove_layer_override(self):
        import maya_ctrls
        reload(maya_ctrls)
        maya_ctrls.remove_layer_override()

    def enable_AOVs(self):
        maya_ctrls.set_aov_enabled_adjust(1)

    def disable_AOVs(self):
        maya_ctrls.set_aov_enabled_adjust(0)

    def warm_tip(self, text):
        message_box = QtGui.QMessageBox()
        message_box.setFixedWidth(300)
        message_box.setText('......Warm Tip......')
        message_box.setIcon(QtGui.QMessageBox.Information)
        message_box.setInformativeText(text)
        message_box.exec_()


class AttributeLayout(QtGui.QGridLayout):
    def __init__(self, name=None, attr_name=None, parent=None):
        super(AttributeLayout, self).__init__(parent)
        self.name = name
        self.attr_name = attr_name
        self.label = QtGui.QLabel(self.name)
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.line = QtGui.QLineEdit()
        self.addWidget(self.label, 0, 0)
        self.addWidget(self.line, 0, 1)
        self.setColumnMinimumWidth(0, 120)
        self.setColumnMinimumWidth(1, 180)


class ProjectWidget(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ProjectWidget, self).__init__(parent)
        self.setWindowTitle('Project')
        self.parent_dir = get_parent_dir()
        main_layout = QtGui.QVBoxLayout(self)
        project_layout = QtGui.QHBoxLayout()
        project_label = QtGui.QLabel('Project Name')
        project_label.setFixedWidth(80)
        self.project_name_cbox = QtGui.QComboBox()
        self.project_name_cbox.setEditable(True)
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_name_cbox)
        separate1 = QtGui.QGroupBox()
        separate1.setFlat(True)
        self.atrribute_layout = QtGui.QGridLayout()
        separate2 = QtGui.QGroupBox()
        separate2.setFlat(True)
        button_layout = QtGui.QHBoxLayout()
        self.accept_btn = QtGui.QPushButton('Accept')
        self.cancel_btn = QtGui.QPushButton('Cancel')
        button_layout.addWidget(self.accept_btn)
        button_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(project_layout)
        main_layout.addWidget(separate1)
        main_layout.addLayout(self.atrribute_layout)
        main_layout.addWidget(separate2)
        main_layout.addLayout(button_layout)
        self.add_attrs()
        self.init_settings()
        self.set_signals()

    def set_signals(self):
        self.accept_btn.clicked.connect(self.add_projcet)
        self.cancel_btn.clicked.connect(self.do_close)
        self.project_name_cbox.currentIndexChanged.connect(self.show_attr)

    def add_attrs(self):
        i = 0
        sample_attrs = [['Camera(AA)', 'defaultArnoldRenderOptions.AASamples'],
                 ['Diffuse', 'defaultArnoldRenderOptions.GIDiffuseSamples'],
                 ['Glossy', 'defaultArnoldRenderOptions.GIGlossySamples'],
                 ['Refraction', 'defaultArnoldRenderOptions.GIRefractionSamples'],
                 ['SSS', 'defaultArnoldRenderOptions.sssBssrdfSamples']]
        for attr in sample_attrs:
            attr_layout = AttributeLayout(attr[0], attr[1])
            self.atrribute_layout.addLayout(attr_layout, i, 0)
            i += 1
        attr_separate = QtGui.QGroupBox('Ray Depth')
        attr_separate.setFlat(True)
        self.atrribute_layout.addWidget(attr_separate, i, 0)
        i += 1
        ray_depth_attrs = [['Total', 'defaultArnoldRenderOptions.GITotalDepth'],
                           ['Diffuse', 'defaultArnoldRenderOptions.GIDiffuseDepth'],
                           ['Glossy', 'defaultArnoldRenderOptions.GIGlossyDepth'],
                           ['Reflection', 'defaultArnoldRenderOptions.GIReflectionDepth'],
                           ['Refraction', 'defaultArnoldRenderOptions.GIRefractionDepth']]
        for attr in ray_depth_attrs:
            attr_layout = AttributeLayout(attr[0], attr[1])
            self.atrribute_layout.addLayout(attr_layout, i, 0)
            i += 1
        motion_blur_separate = QtGui.QGroupBox('Motion Blur')
        motion_blur_separate.setFlat(True)
        self.atrribute_layout.addWidget(motion_blur_separate, i, 0)
        i += 1
        motion_blur_attrs = [['Keys', 'defaultArnoldRenderOptions.motion_steps'],
                             ['Length', 'defaultArnoldRenderOptions.motion_frames']]
        for attr in motion_blur_attrs:
            attr_layout = AttributeLayout(attr[0], attr[1])
            self.atrribute_layout.addLayout(attr_layout, i, 0)
            i += 1
        image_size_separae = QtGui.QGroupBox('Image Size')
        image_size_separae.setFlat(True)
        self.atrribute_layout.addWidget(image_size_separae, i, 0)
        i += 1
        image_size_attrs = [['Width', 'defaultResolution.width'],
                            ['Height', 'defaultResolution.height'],
                            ['Device aspect ratio', 'defaultResolution.deviceAspectRatio'],
                            ['Pixel aspect ratio', 'defaultResolution.pixelAspect']]
        for attr in image_size_attrs:
            attr_layout = AttributeLayout(attr[0], attr[1])
            self.atrribute_layout.addLayout(attr_layout, i, 0)
            i += 1
            
    def init_settings(self):
        project_ini_path = os.path.join(self.parent_dir, 'ini', 'project.data')
        if os.path.isfile(project_ini_path):
            project_names = cpickle_operation.get_cpickle_data(project_ini_path)
            if project_names:
                model = QtGui.QStandardItemModel()
                for project_name in project_names:
                    item = QtGui.QStandardItem(project_name)
                    model.appendRow(item)
                self.project_name_cbox.setModel(model)
                self.project_name_cbox.setCurrentIndex(self.project_name_cbox.count() + 1)

    def add_projcet(self):
        project_name = self.project_name_cbox.currentText()
        if project_name:
            ########project ini path
            project_ini_path = os.path.join(self.parent_dir, 'ini', 'project.data')
            if not os.path.isfile(project_ini_path):
                f = open(os.path.join(self.parent_dir, 'ini', 'project.data'), 'w')
                f.close()
            project_names = cpickle_operation.get_cpickle_data(project_ini_path)
            if project_name not in project_names:
                project_names.append(project_name)
                cpickle_operation.set_cpickle_data(project_ini_path, project_names)
            ########project render settings data
            render_settings_data_dir = os.path.join(self.parent_dir, 'data', 'render_settings_data')
            if not os.path.isdir(render_settings_data_dir):
                os.makedirs(render_settings_data_dir)
            render_settings_data_path = os.path.join(render_settings_data_dir, str(project_name)+'_render_settings.json')
            render_settings_dict = dict()
            for i in xrange(self.atrribute_layout.count()):
                layout = self.atrribute_layout.itemAt(i).layout()
                if layout and layout.line.text():
                    render_settings_dict[layout.attr_name] = str(layout.line.text())
            json_operation.set_json_data(render_settings_data_path, render_settings_dict)
        else:
            warm_tip.warm_tip('Please input a project name')
        try:
            rsw_widget.update_project()
        except:pass
        self.do_close()
        
    def show_attr(self):
        project_name = str(self.project_name_cbox.currentText())
        if project_name:
            render_settings_data_dir = os.path.join(self.parent_dir, 'data', 'render_settings_data')
            render_settings_data_path = os.path.join(render_settings_data_dir, project_name+'_render_settings.json')
            if os.path.isfile(render_settings_data_path):
                json_data = json_operation.get_json_data(render_settings_data_path)
                for data in json_data:
                    for i in xrange(self.atrribute_layout.count()):
                        layout = self.atrribute_layout.itemAt(i).layout()
                        if layout and layout.attr_name == data:
                            layout.line.setText(json_data[data])

    def do_close(self):
        self.close()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.close()


def run():
    global rsw_widget
    try:
        rsw_widget.close()
        rsw_widget.deleteLater()
    except:pass
    rsw_widget = RenderSettingsWidget(public_ctrls.get_maya_win())
    rsw_widget.show()
