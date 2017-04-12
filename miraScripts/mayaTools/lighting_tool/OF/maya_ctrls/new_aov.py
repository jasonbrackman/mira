from PySide import QtGui, QtCore
import maya.OpenMayaUI as mui
import mtoa.aovs as aovs
import maya.cmds as mc
import pymel.core as pm
import re
import mtoa.ui.ae.shaderTemplate as st
import mtoa.ui.ae.shadingEngineTemplate as se
import time


pass_dict = dict(red   = ['#FF0000', [1, 0, 0]],
                 green = ['#00FF00', [0, 1, 0]],
                 blue  = ['#0000FF', [0, 0, 1]],
                 black = ['#000000', [0, 0, 0]],
                 rim   = ['#FFFFFF', [1, 1, 1]]
                )
                
window_name = 'AOV Settings'


class CheckStatus(object):
    status = False


class Utils(object):
    MASK_PATTERN = re.compile(r'^mask(\d+)$')
    MASK_PATTERN2 = re.compile(r'.*:?(mask\d+)_\w+')

    @staticmethod
    def get_maya_win():
        ptr = mui.MQtUtil.mainWindow()
        if 'PyQt4' in QtGui.__name__:
            import sip
            main_window = sip.wrapinstance(long(ptr), QtCore.QObject)
        if 'PySide' in QtGui.__name__:
            import shiboken
            main_window = shiboken.wrapInstance(long(ptr), QtCore.QObject)
        return main_window

    @staticmethod
    def get_aov_name_lists():
        return [i.name for i in aovs.getAOVs()]

    @staticmethod
    def get_object_list():
        selected_objects = []
        for i in pm.ls(sl=1):
            if i.type() in ['mesh', 'nurbsSurface']:
                selected_objects.append(i)
            else:
                if i.type() == 'transform':
                    children = pm.ls(i, ap=1, dag=1, lf=1)
                    for child in children:
                        if child.type() in ['mesh', 'nurbsSurface'] and not child.name().endswith('Orig'):
                            selected_objects.append(child)
        selected_objects = list(set(selected_objects))
        return selected_objects

    @staticmethod
    def get_hair_list():
        selected_objects = []
        if pm.ls(sl=1):
            for i in pm.ls(sl=1):
                if i.type() in ['pfxHair']:
                    selected_objects.append(i)
                else:
                    if i.type() == 'transform':
                        children = pm.ls(i, ap=1, dag=1, lf=1)
                        for child in children:
                            if child.type() in ['pfxHair']:
                                selected_objects.append(child)
        return selected_objects

    @staticmethod
    def add_attribute(mesh, aov_name, color):
        if aov_name.startswith('mask'):
            if not hasattr(mesh, 'mtoa_constant_%s' % aov_name):
                pm.addAttr(mesh, ln='mtoa_constant_%s' % aov_name, at='double3')
                pm.addAttr(mesh, ln='mtoa_constant_%sX' % aov_name, at='double', parent='mtoa_constant_%s' % aov_name)
                pm.addAttr(mesh, ln='mtoa_constant_%sY' % aov_name, at='double', parent='mtoa_constant_%s' % aov_name)
                pm.addAttr(mesh, ln='mtoa_constant_%sZ' % aov_name, at='double', parent='mtoa_constant_%s' % aov_name)
            pm.setAttr('%s.mtoa_constant_%s' % (mesh.name(), aov_name), pass_dict[color][1], type='double3')

    @staticmethod
    def get_sg_node_of_mesh(mesh):
        return mesh.outputs(type='shadingEngine')

    @classmethod
    def get_sg_node_of_selected(cls):
        sg_nodes = []
        all_meshes = cls.get_object_list()
        if all_meshes:
            for mesh in all_meshes:
                sg_nodes.extend(cls.get_sg_node_of_mesh(mesh))
        sg_nodes = list(set(sg_nodes))
        return sg_nodes

    @staticmethod
    def create_shader(color_name):
        if color_name == "rim":
            shader_name = "aiOf_aiRimFilter"
        else:
            shader_name = "aiUtility"
        if not pm.objExists(color_name+'_SHD'):
            shader = pm.shadingNode(shader_name, asShader=True, name=(color_name+'_SHD').upper())
        else:
            shader = pm.PyNode(color_name+'_SHD')
        if color_name == "rim":
            shader.Exp.set(6)
            shader.BaseColor.set([0, 0, 0])
        else:
            shader.color.set(pass_dict[color_name][1], type="double3")
            shader.shadeMode.set(2)
        return shader

    @staticmethod
    def current_render():
        return pm.PyNode("defaultRenderGlobals").currentRenderer.get()

    @staticmethod
    def get_aov_index(sg_node, aov_name):
        aov_list = [i.aovName.get() for i in sg_node.aiCustomAOVs]
        if aov_name not in aov_list:
            se.ShadingEngineTemplate("shadingEngine").updateAOVFrame(sg_node.aiCustomAOVs)
            print '[updating shadingEngineTemplate]'
            aov_list = [i.aovName.get() for i in sg_node.aiCustomAOVs]
        return aov_list.index(aov_name)

    @staticmethod
    def get_opacity_attr_of_sg_node(sg_node):
        shader = opacity_attr = None
        try:
            shader = pm.listConnections(sg_node.surfaceShader, source=1, destination=0)[0]
        except:pass
        if shader:
            try:
                opacity_attr = pm.listConnections(shader.opacity, source=1, destination=0, plugs=1)[0]
            except:pass
        return opacity_attr

    @classmethod
    def get_sg_node_of_opacity(cls):
        sg_nodes_of_opacity = []
        for sg_node in pm.ls(type='shadingEngine'):
            if cls.get_opacity_attr_of_sg_node(sg_node):
                sg_nodes_of_opacity.append(sg_node)
        return sg_nodes_of_opacity

    @classmethod
    def connect_shader(cls, *args):
        #args(mask00, red)
        sg_nodes = cls.get_sg_node_of_selected()
        if sg_nodes:
            shader = cls.create_shader(args[1])
            progress_dialog = QtGui.QProgressDialog('<Total: %s>build aov...,Please wait......' % len(sg_nodes),
                                                    'Cancel', 0, len(sg_nodes))
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()
            value = 0
            for i in sg_nodes:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                    break
                index = cls.get_aov_index(i, args[0])
                if args[0] == 'rim':
                    shader.outColor >> i.aiCustomAOVs[index].aovInput
                    print '[connect shader] %s >> %s.%s' % (shader, i, args[0])
                    value += 1

    @staticmethod
    def create_common_shader(name):
        if name == 'AO':
            shader_type = 'aiAmbientOcclusion'
            shader_name = 'AO_aov_default_shader'.upper()
        if not pm.objExists(shader_name):
            shader = pm.shadingNode(shader_type, asShader=True, name=shader_name)
        else:
            shader = pm.PyNode(shader_name)
        if name == 'rim':
            shader.Exp.set(6)
            shader.BaseColor.set([0, 0, 0])
        return shader

    @staticmethod
    def create_new_common_shader(name):
        if name == 'AO':
            shader_type = 'aiAmbientOcclusion'
            shader_name = 'AO_aov_shader_new'.upper()
        shader = pm.shadingNode(shader_type, asShader=True, name=shader_name)
        return shader

    @staticmethod
    def create_aiUtility_shader(emission_name='emission_aiUtility'.upper()):
        shader = pm.shadingNode('aiUtility', asShader=True, name=emission_name)
        shader.shadeMode.set(2)
        return shader

    @staticmethod
    def create_aistandard_shader(emission_name='emission_aiStandard'.upper()):
        shader = pm.shadingNode('aiStandard', asShader=True, name=emission_name)
        shader.color.set(0, 0, 0)
        shader.Kd.set(0)
        shader.emission.set(1)
        return shader

    @classmethod
    def connect_emission_shader(cls, mesh, aov_name, color):
        sg_node = mesh.outputs(type='shadingEngine')
        if sg_node:
            sg_node = sg_node[0]
            opacity_attr = cls.get_opacity_attr_of_sg_node(sg_node)
            if opacity_attr:
                index = cls.get_aov_index(sg_node, aov_name)
                emission_standard = sg_node.aiCustomAOVs[index].aovInput.connections()
                if emission_standard and (aov_name+'_emission_aiStandard').upper() in emission_standard[0].name():
                    emission_utility = emission_standard[0].emissionColor.connections()
                    if emission_utility and (aov_name+'_emission_aiUtility').upper() in emission_utility[0].name():
                        emission_utility[0].color.set(pass_dict[color][1])
                else:
                    utility_shader = cls.create_aiUtility_shader((aov_name+'_emission_aiUtility').upper())
                    utility_shader.color.set(pass_dict[color][1])
                    standard_shader = cls.create_aistandard_shader((aov_name+'_emission_aiStandard').upper())
                    standard_shader.aovEmission.set(aov_name)
                    utility_shader.outColor >> standard_shader.emissionColor
                    standard_shader.outColor >> sg_node.aiCustomAOVs[index].aovInput
                    try:
                        pm.connectAttr(opacity_attr, utility_shader.opacity)
                    except:
                        try:
                            pm.connectAttr(opacity_attr.node().outAlpha, utility_shader.opacity)
                        except Exception as e:
                            print e
                    print '[connect shader] %s >> %s.%s' % (standard_shader, sg_node, aov_name)

    @classmethod
    def connect_default_shader(cls, aov_name):
        shader = cls.create_common_shader(aov_name)
        shader.outColor >> pm.PyNode('aiAOV_%s' % aov_name).defaultValue
        print '[OF] info: %s\'s default shader has been connected' % aov_name

    @classmethod
    def connect_common_shader(cls, name):
        sg_nodes = cls.get_sg_node_of_opacity()
        if sg_nodes:
            progress_dialog = QtGui.QProgressDialog('<Total: %s>build aov...,Please wait......' % len(sg_nodes),
                                                    'Cancel', 0, len(sg_nodes))
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()
            value = 0
            for i in sg_nodes:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                    break
                index = cls.get_aov_index(i, name)
                if i.aiCustomAOVs[index].aovInput.connections():
                    if (name+'_emission_shader').upper() in i.aiCustomAOVs[index].aovInput.connections()[0].name():
                        break
                opacity_attr = cls.get_opacity_attr_of_sg_node(i)
                new_shader = cls.create_new_common_shader(name)
                try:
                    pm.connectAttr(opacity_attr, new_shader.opacity)
                except:
                    try:
                        pm.connectAttr(opacity_attr.node().outAlpha, new_shader.opacity)
                    except Exception as e:
                        print e
                aiStandard_shader = cls.create_aistandard_shader(emission_name=(name+'_emission_shader').upper())
                new_shader.outColor >> aiStandard_shader.emissionColor
                aiStandard_shader.aovEmission.set(name)
                aiStandard_shader.outColor >> i.aiCustomAOVs[index].aovInput
                print '[connect shader] %s >> %s.%s' % (aiStandard_shader, i, name)
                value += 1

    @classmethod
    def create_common_aov(cls, name):
        start = time.time()
        cls.add_custom_aov(name)
        cls.connect_default_shader(name)
        print "%s cost %s(s)" % (name, time.time()-start)

    @classmethod
    def add_custom_aov(cls, name):
        if name not in cls.get_aov_name_lists():
            try:
                aovs.AOVInterface().addAOV(name)
            except:pass
        pm.PyNode('aiAOV_%s.type' % name).set(5)
        pm.PyNode('aiAOV_%s.enabled' % name).set(1)
        print "[OF] info: add aov ******%s****** successful" % name
        return name

    @staticmethod
    def create_aiuserdatacolor_shader(aov_name):
        shader_name = ('%s_aiuserdatacolor' % aov_name).upper()
        if not pm.objExists(shader_name):
            shader = pm.shadingNode('aiUserDataColor', asShader=1, name=shader_name)
            shader.colorAttrName.set(aov_name)
        else:
            shader = pm.PyNode(shader_name)
        return shader

    @classmethod
    def add_mask_aov(cls):
        aov_lists = [int(cls.MASK_PATTERN.findall(i)[0])
                     for i in cls.get_aov_name_lists() if cls.MASK_PATTERN.findall(i)]
        if not aov_lists:
            new_aov = "mask00"
        else:
            new_aov = "mask%02d" % (sorted(aov_lists)[-1]+1)
        try:
            aovs.AOVInterface().addAOV(new_aov)
        except:pass
        print "[OF] info: add aov ******%s****** successful" % new_aov
        pm.PyNode('aiAOV_%s.type' % new_aov).set(5)
        shader = cls.create_aiuserdatacolor_shader(new_aov)
        shader.outColor >> pm.PyNode('aiAOV_%s' % new_aov).defaultValue
        return new_aov

    @classmethod
    def init_connect_default_shader(cls):
        for aov in cls.get_aov_name_lists():
            if aov == 'AO':
                ao_pattern = r'.*AO_AOV_DEFAULT_SHADER$'
                default_shader = default_mask_shader = None
                for shader in mc.ls(materials=1):
                    if re.match(ao_pattern, shader):
                        default_shader = re.match(ao_pattern, shader).group()
                        pm.PyNode(default_shader).outColor >> pm.PyNode('aiAOV_AO').defaultValue
                        print '[OF] info:%s >> AO.defaultValue' % default_shader
                        break
                if not default_shader:
                    default_shader = cls.create_common_shader('AO')
                    default_shader.outColor >> pm.PyNode('aiAOV_AO').defaultValue
            if aov.startswith('mask'):
                mask_pattern = r'.*%s_AIUSERDATACOLOR$' % aov.upper()
                for shader in mc.ls(materials=1):
                    if re.match(mask_pattern, shader):
                        default_mask_shader = re.match(mask_pattern, shader).group()
                        pm.PyNode(default_mask_shader).outColor >> pm.PyNode('aiAOV_%s' % aov).defaultValue
                        print '[OF] info:%s >> %s.defaultValue' % (default_mask_shader, aov)
                        break
                if not default_mask_shader:
                    default_mask_shader = cls.create_aiuserdatacolor_shader(aov)
                    default_mask_shader.outColor >> pm.PyNode('aiAOV_%s' % aov).defaultValue

    @classmethod
    def rebuild_arnold_aov(cls):
        # arnold rebuild aov
        aov_lists = list()
        # get shading group's aovname
        sg_nodes = pm.ls(type='shadingEngine')
        if len(sg_nodes) > 200:
            sg_nodes = sg_nodes[:200]
        progress_dialog = QtGui.QProgressDialog('<Total: %s>build aov...,Please wait......' % len(sg_nodes),
                                                'Cancel', 0, len(sg_nodes))
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.show()
        value = 0
        for se in sg_nodes:
            progress_dialog.setValue(value)
            if progress_dialog.wasCanceled():
                return
            for aov in se.aiCustomAOVs:
                print '[OF] Info:find', aov, aov.aovName.get()
                aov_lists.append(aov.aovName.get())
            value += 1
        # get aiWriteColor's aov_name
        if pm.ls(type='aiWriteColor'):
            for wc in pm.ls(type='aiWriteColor'):
                print wc.aovName.get()
                m = re.compile('(.*) \(Inactive\)').match(wc.aovName.get())
                if m:
                    print '[OF] Info:find', wc, wc.aovName.get()
                    aov_lists.append(m.groups()[0])
                else:
                    if wc.aovName.get():
                        print '[OF] Info:find', wc, wc.aovName.get()
                        aov_lists.append(wc.aovName.get())
        #get aiUserDataColor's aov_name
        if pm.ls(type='aiUserDataColor'):
            for node in pm.ls(type='aiUserDataColor'):
                print "[OF] info:find %s" % node.colorAttrName.get()
                aov_lists.append(node.colorAttrName.get())

        aov_lists = list(set(aov_lists))
        for aov in aov_lists:
            if aov and aov not in cls.get_aov_name_lists():
                try:
                    aovs.AOVInterface().addAOV(aov)
                    print '[OF] Info: Rebuild %s' % aov
                except:pass
        for aov in cls.get_aov_name_lists():
            if aov.startswith('mask') or aov.startswith('rim'):
                mc.setAttr('aiAOV_%s.type' % aov, 5)

        cls.init_connect_default_shader()


class ColorButton(QtGui.QPushButton):
    kick = QtCore.Signal(list)

    def __init__(self, text=None, parent=None):
        super(ColorButton, self).__init__(parent)
        self.text = text
        self.menu = QtGui.QMenu()
        self.action = None
        self.setFixedHeight(30)
        self.setText(self.text)
        self.setStyleSheet("QPushButton{color:#FFFFFF;background: %s}" % pass_dict[self.text][0])
        self.pressed.connect(self.set_menu)

    def set_menu(self):
        self.menu.clear()
        for aov in [aov for aov in Utils.get_aov_name_lists() if aov.startswith('mask')
                    or aov.startswith('rim')]:
            self.action = QtGui.QAction(aov, self)
            self.action.triggered.connect(self.connect_aov)
            self.menu.addAction(self.action)
        self.menu.exec_(QtGui.QCursor.pos())

    def connect_aov(self):
        aov_name = str(self.sender().text())
        if aov_name == 'rim':
            if not CheckStatus.status:
                Utils.connect_shader('rim', 'rim')
                self.kick.emit([1, '//[OF] info: Connect Rim Successful'])
            else:
                self.kick.emit([0, '//[OF] info: Hair has no rim aov'])
        elif aov_name.startswith('mask'):
            if not CheckStatus.status:
                selected_meshes = Utils.get_object_list()
                if selected_meshes:
                    for mesh in selected_meshes:
                        Utils.add_attribute(mesh, aov_name, self.text)
                        Utils.connect_emission_shader(mesh, aov_name, self.text)
                    self.kick.emit([1, '//[OF] info: Connect %s Successful' % aov_name])
                else:
                    self.kick.emit([0, '//[OF] error: Nothing Selected'])
            else:
                selected_meshes = Utils.get_hair_list()
                if selected_meshes:
                    for mesh in selected_meshes:
                        Utils.add_attribute(mesh, aov_name, self.text)
                    self.kick.emit([1, '//[OF] info: Connect %s Successful' % aov_name])
                else:
                    self.kick.emit([0, '//[OF] error: Nothing Selected'])


class CommonAovButton(QtGui.QPushButton):
    kick = QtCore.Signal(str)

    def __init__(self, text=None, parent=None):
        super(CommonAovButton, self).__init__(parent)
        self.text = text
        self.setText(self.text)
        self.pressed.connect(self.create_common_aov_menu)
        self.create_menu = QtGui.QMenu()
        self.attr_menu = QtGui.QMenu()

    def create_common_aov_menu(self):
        self.create_menu.clear()
        for aov in ['AO']:
            action = QtGui.QAction(aov, self)
            action.triggered.connect(self.create_common_aov)
            self.create_menu.addAction(action)
        self.create_menu.exec_(QtGui.QCursor.pos())

    def contextMenuEvent(self, event):
        self.attr_menu.clear()
        for attr in ['Set AO samples']:
            action = QtGui.QAction(attr, self)
            action.triggered.connect(self.set_attr)
            self.attr_menu.addAction(action)
        self.attr_menu.exec_(QtGui.QCursor.pos())

    def create_common_aov(self):
        Utils.create_common_aov(str(self.sender().text()))
        Utils.connect_common_shader(str(self.sender().text()))
        self.kick.emit('//[OF] info: %s aov create successful !!!' % self.sender().text())

    def set_attr(self):
        if str(self.sender().text()) == 'Set AO samples':
            self.set_ao_samples()

    def set_ao_samples(self):
        sample_value = 3
        try:
            sample_value = pm.PyNode('AO_AOV_DEFAULT_SHADER').samples.get()
        except:pass
        if mc.window('set ao samples', q=1, ex=1):
            mc.deleteUI('set ao samples')
        mc.window('set ao samples', title='set ao samples')
        mc.columnLayout()
        mc.intSliderGrp('ao_samples_slider', label='AO Samples', field=True, minValue=0, maxValue=10, value=sample_value,
                        sliderStep=1, fieldMaxValue=100.0, changeCommand=pm.Callback(self.set_samples))
        mc.showWindow()

    def set_samples(self):
        value = mc.intSliderGrp('ao_samples_slider', value=1, q=1)
        if pm.ls(type='aiAmbientOcclusion'):
            for i in pm.ls(type='aiAmbientOcclusion'):
                i.samples.set(value)
                print "[OF] info: set %s.samples" % i, value
        self.kick.emit("[OF] info: set AO samples %s" % value)


class View(QtGui.QDialog):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.resize(510, 100)
        self.setWindowTitle('AOV Settings')
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint)
        
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 2)
        main_layout.setSpacing(0)
        
        display_frame = QtGui.QFrame()
        display_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout_of_frame = QtGui.QHBoxLayout(display_frame)
        layout_of_frame.setContentsMargins(0, 0, 0, 0)
        self.display_label = QtGui.QLabel()
        self.display_label.setFixedHeight(35)
        self.check_box = QtGui.QCheckBox('Hair')
        self.check_box.setChecked(False)
        layout_of_frame.addWidget(self.display_label)
        layout_of_frame.addStretch()
        layout_of_frame.addWidget(self.check_box)
        
        create_frame = QtGui.QFrame()
        create_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        create_layout = QtGui.QHBoxLayout(create_frame)
        create_layout.setContentsMargins(0, 0, 0, 0)
        create_layout.setSpacing(1)
        self.create_mask_aov_btn = QtGui.QPushButton('Mask AOV')
        self.create_mask_aov_btn.setFixedHeight(30)
        self.create_rim_aov_btn = QtGui.QPushButton('Rim AOV')
        self.create_rim_aov_btn.setFixedHeight(30)
        self.create_common_aov_btn = CommonAovButton('Common AOV')
        self.create_common_aov_btn.setFixedHeight(30)
        self.create_custom_aov_btn = QtGui.QPushButton('Custom AOV')
        self.create_custom_aov_btn.setFixedHeight(30)
        self.rebuild_aov_btn = QtGui.QPushButton('Rebuild AOV')
        self.rebuild_aov_btn.setFixedHeight(30)
        create_layout.addWidget(self.create_mask_aov_btn)
        create_layout.addWidget(self.create_rim_aov_btn)
        create_layout.addWidget(self.create_common_aov_btn)
        create_layout.addWidget(self.create_custom_aov_btn)
        create_layout.addWidget(self.rebuild_aov_btn)
        
        separator_btn = QtGui.QPushButton()
        separator_btn.setFixedHeight(8)
        separator_btn.setEnabled(False)
        
        button_frame = QtGui.QFrame()
        button_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        self.color_btn_layout = QtGui.QHBoxLayout(button_frame)
        self.color_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.color_btn_layout.setSpacing(1)
        
        main_layout.addWidget(display_frame)
        main_layout.addWidget(create_frame)
        main_layout.addWidget(separator_btn)
        main_layout.addWidget(button_frame)
        

class AovSettings(View):
    def __init__(self, parent=None):
        super(AovSettings, self).__init__(parent)
        self.setObjectName(window_name)
        self.btn = None
        self.init_settings()
        self.set_signals()
        
    def init_settings(self):
        self.display_label.setText('<font color=#00FF00><b> ^o^ Welcome to use !!!</b></font>')
        all_pass = ['red', 'green', 'blue', 'black', 'rim']
        for color in all_pass:
            self.btn = ColorButton(color)
            if color == 'rim':
                self.btn.setStyleSheet('QPushButton{color:#000000; background:#FFFFFF}')
            self.btn.kick.connect(self.show_status)
            self.color_btn_layout.addWidget(self.btn)
            
    def set_signals(self):
        self.create_mask_aov_btn.clicked.connect(self.create_mask_aov)
        self.create_rim_aov_btn.clicked.connect(self.create_rim_aov)
        self.create_common_aov_btn.kick.connect(self.show_status)
        self.create_custom_aov_btn.clicked.connect(self.create_custom_aov)
        self.rebuild_aov_btn.clicked.connect(self.rebuild_aov)
        self.check_box.stateChanged.connect(self.set_status_global)

    @staticmethod
    def set_status_global(status):
        if status:
            CheckStatus.status = True
        else:
            CheckStatus.status = False

    def show_status(self, value):
        if isinstance(value, list):
            if value[0]:
                self.display_label.setText('<font color=#00FF00><b> %s </b></font>' % value[1])
            else:
                self.display_label.setText('<font color=#FF0000><b> %s </b></font>' % value[1])
        if isinstance(value, basestring):
            self.display_label.setText('<font color=#00FF00><b> %s </b></font>' % value)

    def create_mask_aov(self):
        new_aov = Utils.add_mask_aov()
        self.display_label.setText('<font color=#00FF00><b>//[OF] info: %s aov create successful !!!</b></font>' % new_aov)

    def create_rim_aov(self):
        Utils.add_custom_aov('rim')
        self.display_label.setText('<font color=#00FF00><b>//[OF] info: rim aov create successful !!!</b></font>')

    def create_custom_aov(self):
        aov_name = st.newAOVPrompt()
        if aov_name:
            self.display_label.setText('<font color=#00FF00><b>//[OF] info: %s aov create successful!!!</b></font>' % aov_name[0])
        else:
            self.display_label.setText('')

    def rebuild_aov(self):
        Utils.rebuild_arnold_aov()
        self.display_label.setText('<font color=#00FF00><b>//[OF] info: Rebuild Successful !!!</b></font>')

    @classmethod
    def show_ui(cls):
        if Utils.current_render() != 'arnold':
            QtGui.QMessageBox.information(None, 'Information', 'Current renderer is not arnold')
        else:
            if mc.window(window_name, q=1, exists=1):
                mc.deleteUI(window_name)
            dialog = cls(Utils.get_maya_win())
            dialog.show()
            
            
if __name__ == '__main__':
    AovSettings.show_ui()