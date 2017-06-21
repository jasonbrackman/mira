#! /usr/bin/env python
#coding=utf-8
#
# dev path = python/object_render_pass/object_render_pass.py
# modified by Yan-Chen Liao, Heshuai
#
# Usage:
#import lightingTools.object_render_pass
#reload(lightingTools.object_render_pass)
#lightingTools.object_render_pass.main()

import re
import pymel.core as pm
import maya.cmds as mc
import mtoa.aovs as aovs
import mtoa.ui.ae.shadingEngineTemplate as se
import mtoa.ui.ae.shaderTemplate as st
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import time


alofhair_aovs = ['diffuse_color', 'direct_glint', 'direct_global', 'direct_local', 'direct_specular_2',
                 'direct_transmission', 'indirect_global', 'indirect_local', 'indirect_specular_2',
                 'indirect_transmission', 'indirect_glint']


def set_template():
    template = pm.uiTemplate('tim_template', force=1)
    template.define(pm.window, edit=1, resizeToFitChildren=1)
    template.define(pm.button, width=100, height=30, align='left')
    template.define(pm.frameLayout, borderVisible=1, labelVisible=0, height=35,
        borderStyle="etchedIn")
    template.define(pm.rowLayout, columnAlign1=('left'), height=30)
    template.define(pm.text, align='left', height=30)

    return template


class ObjectRenderPass():
    MASK_PATTERN = re.compile(r'^mask(\d+)$')
    HAIR_PATTERN = re.compile(r'^hair(\d+)$')
    ALL_PATTERN = re.compile(r'^all(\d+)$')
    MASK_PATTERN2 = re.compile(r'.*:?(mask\d+)_\w+')

    def __init__(self):
        self.render_settings = pm.PyNode("defaultRenderGlobals")
        self.show_window()

    def show_window(self):
        window_name = "设置通道".decode("utf-8")
        self.pass_dict = {'red': ["红".decode("utf-8"), [1, 0, 0]],
                          'green': ["绿".decode("utf-8"), [0, 1, 0]],
                          'black': ["黑".decode("utf-8"), [0, 0, 0]],
                          'blue': ["蓝".decode("utf-8"), [0, 0, 1]],
                          'rim': ["边缘光".decode("utf-8"), [1, 1, 1]]
                          }
        self.pop = {}

        if pm.window(window_name, q=1, ex=1):
            pm.deleteUI(window_name)
        if pm.windowPref(window_name, exists=1):
            pm.windowPref(window_name, remove=1)

        with pm.window(window_name):
            with set_template():
                with pm.frameLayout():
                    with pm.rowLayout(numberOfColumns=3, columnWidth3=[420, 50, 50]):
                        self.renderer = self.render_settings.currentRenderer.get()
                        pm.text('info_text', label='')
                        self.show_sg_attrs()
                        pm.checkBox('hair_check', label='hair', onCommand=pm.Callback(self.show_hair_attrs),
                                    offCommand=pm.Callback(self.show_sg_attrs))
                        pm.checkBox('all_check', label='all', onCommand=pm.Callback(self.show_all_attrs),
                                    offCommand=pm.Callback(self.show_sg_attrs))

                with pm.frameLayout():
                    with pm.rowLayout(numberOfColumns=5):
                        pm.button('create_aov', label="创建mask aov".decode("utf-8"), command=self.add_mask_aov)
                        if self.renderer == "arnold":
                            rim_btn = pm.button(label="创建rim aov".decode('utf-8'), command=self.add_rim_aov)
                            costom_btn = pm.button(label="创建常用aov".decode("utf-8"))
                            popup_menu_left = pm.popupMenu(parent=costom_btn, button=1)
                            pm.menuItem(parent=popup_menu_left, label='AO',
                                        command=pm.Callback(self.create_costom_aov, "AO"))
                            pm.menuItem(parent=popup_menu_left, label='ambocc',
                                        command=pm.Callback(self.create_costom_aov, "ambocc"))
                            pm.menuItem(parent=popup_menu_left, label='lambert',
                                        command=pm.Callback(self.create_costom_aov, "lambert"))
                            popup_menu_right = pm.popupMenu(parent=costom_btn, button=3)
                            pm.menuItem(parent=popup_menu_right, label='Set AO samples',
                                        command=self.set_ao_samples)
                        pm.button(label="创建自定义aov".decode("utf-8"), command=self.add_custom_aov)
                        if self.renderer == "mentalRay":
                            pm.button(label=u"重建aov", command=self.rebuld_aov)
                        elif self.renderer == 'arnold':
                            pm.button(label=u"重建aov", command=self.rebuild_arnold_aov_final)

                with pm.frameLayout():
                    with pm.rowLayout(numberOfColumns=len(self.pass_dict)):
                        all_pass = ["red", "green", "blue", "black", "rim"]
                        if self.renderer == "mentalRay":
                            all_pass = all_pass[:-1]

                        for i in all_pass:
                            pm.button(label=self.pass_dict[i][0],
                                      backgroundColor=self.pass_dict[i][1])
                            self.pop[i] = pm.popupMenu(button=1,
                                                       postMenuCommand=pm.Callback(self.show_aov_lists, i))

    def show_hair_attrs(self):
        pm.checkBox('all_check', e=1, value=0)
        try:
            pm.button('create_aov', e=1, label="创建hair aov".decode("utf-8"))
        except:pass
        num_hairs = len(pm.ls(type='pfxHair'))+len(pm.ls(type='shaveHair'))+len(pm.ls(type='pgYetiMaya'))
        pm.text('info_text', e=1, backgroundColor=[1, 0.5, 1],
                label="当前使用的渲染器: %s     ==|===========>     毛发的数量：%s".decode("utf-8") % (self.renderer, num_hairs))

    def show_sg_attrs(self):
        try:
            pm.button('create_aov', e=1, label="创建mask aov".decode("utf-8"))
        except:pass
        sg_num = len(pm.ls(type='shadingEngine'))
        pm.text('info_text', e=1, backgroundColor=[0.27, 0.27, 0.27],
                label="当前使用的渲染器: %s     ==|===========>     sg节点的数量：%s".decode("utf-8") % (self.renderer, sg_num))

    def show_all_attrs(self):
        pm.checkBox('hair_check', e=1, value=0)
        try:
            pm.button('create_aov', e=1, label="创建all aov".decode("utf-8"))
        except:pass
        all_num = len(pm.ls(sl=1))
        pm.text('info_text', e=1, backgroundColor=[0.5, 0.5, 1],
                label="当前使用的渲染器: %s     ==|===========>     节点的数量：%s".decode("utf-8") % (self.renderer, all_num))
                                
    def rebuild_arnold_aov(self, *args):
        # arnold rebuild aov
        aov_lists = list()
        # get shading group's aovname
        sg_nodes = pm.ls(type='shadingEngine')
        #if len(sg_nodes) > 200:
        #    sg_nodes = sg_nodes[:200]
        progress_dialog = QProgressDialog('<Total: %s>build aov...,Please wait......' % len(sg_nodes), 'Cancel', 0, len(sg_nodes))
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()
        value = 0
        for sg in sg_nodes:
            progress_dialog.setValue(value)
            if progress_dialog.wasCanceled():
                break
            for aov in sg.aiCustomAOVs:
                print '[OF] Info:find', aov, aov.aovName.get()
                aov_lists.append(aov.aovName.get())
            value += 1
        # get aiWriteColor's aovname
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
            if aov and aov not in self.get_aov_name_lists():
                if aov not in alofhair_aovs:
                    try:
                        aovs.AOVInterface().addAOV(aov)
                        print '[OF] Info: Rebuild %s' % aov
                    except:pass
                
        for aov in self.get_aov_name_lists():
            if aov.startswith('mask') or aov.startswith('rim'):
                mc.setAttr('aiAOV_%s.type' % aov, 5)
    
    def connect_mask_aov_default_shader(self):
        shader = self.create_default_mask_aov_shader()
        for aov in self.get_aov_name_lists():
            if aov.startswith('mask') or aov.startswith('rim'):
                mc.setAttr('aiAOV_%s.type' % aov, 5)
                try:
                    shader.outColor >> pm.PyNode('aiAOV_%s' % aov).defaultValue
                    print '[OF] info: %s >> %s.default shader' % (shader.name(), aov)
                except:pass
            elif aov.startswith('hair') or aov.startswith('all'):
                mc.setAttr('aiAOV_%s.type' % aov, 5)
                hair_shader = self.create_aiuserdatacolor_shader(aov)
                try:
                    hair_shader.outColor >> pm.PyNode('aiAOV_%s' % aov).defaultValue
                    print '[OF] info: %s >> %s.default shader' % (hair_shader.name(), aov)
                except:pass

    def rebuild_arnold_aov_final(self, *args):
        self.rebuild_arnold_aov()
        self.connect_mask_aov_default_shader()

    def create_default_mask_aov_shader(self):
        if not pm.objExists('DEFAULT_MASK_AOV_SHADER'):
            shader = pm.shadingNode('surfaceShader', asShader=1, name='DEFAULT_MASK_AOV_SHADER')
            shader.outMatteOpacity.set(0, 0, 0)
        else:
            shader = pm.PyNode('DEFAULT_MASK_AOV_SHADER')
        return shader

    def create_aiuserdatacolor_shader(self, aov_name):
        shader_name = ('%s_aiuserdatacolor' % aov_name).upper()
        if not pm.objExists(shader_name):
            shader = pm.shadingNode('aiUserDataColor', asShader=1, name=shader_name)
            shader.colorAttrName.set(aov_name)
        else:
            shader = pm.PyNode(shader_name)
        return shader

    def add_attribute(self, mesh, aov_name, color):
        if aov_name.startswith('hair') or aov_name.startswith('all'):
            if not hasattr(mesh, 'mtoa_constant_%s' % aov_name):
                pm.addAttr(mesh, ln='mtoa_constant_%s' % aov_name, at='double3')
                pm.addAttr(mesh, ln='mtoa_constant_%sX' % aov_name, at='double', parent='mtoa_constant_%s' % aov_name)
                pm.addAttr(mesh, ln='mtoa_constant_%sY' % aov_name, at='double', parent='mtoa_constant_%s' % aov_name)
                pm.addAttr(mesh, ln='mtoa_constant_%sZ' % aov_name, at='double', parent='mtoa_constant_%s' % aov_name)
            pm.setAttr('%s.mtoa_constant_%s' % (mesh.name(), aov_name), self.pass_dict[color][1], type='double3')

    def add_mask_aov(self, *args):
        aov_lists = [int(self.MASK_PATTERN.findall(i)[0])
                     for i in self.get_aov_name_lists() if self.MASK_PATTERN.findall(i)]
        hair_aov_lists = [int(self.HAIR_PATTERN.findall(i)[0])
                          for i in self.get_aov_name_lists() if self.HAIR_PATTERN.findall(i)]
        all_aov_lists = [int(self.ALL_PATTERN.findall(i)[0])
                          for i in self.get_aov_name_lists() if self.ALL_PATTERN.findall(i)]
        if self.renderer == "arnold":
            if not pm.checkBox('hair_check', q=1, value=1) and not pm.checkBox('all_check', q=1, value=1):
                shader = self.create_default_mask_aov_shader()
                if not aov_lists:
                    new_aov = "mask00"
                else:
                    new_aov = "mask%02d" % (sorted(aov_lists)[-1]+1)
            if pm.checkBox('hair_check', q=1, value=1):
                if not hair_aov_lists:
                    new_aov = 'hair00'
                else:
                    new_aov = "hair%02d" % (sorted(hair_aov_lists)[-1]+1)
                shader = self.create_aiuserdatacolor_shader(new_aov)
            if pm.checkBox('all_check', q=1, value=1):
                if not all_aov_lists:
                    new_aov = 'all00'
                else:
                    new_aov = "all%02d" % (sorted(all_aov_lists)[-1]+1)
                shader = self.create_aiuserdatacolor_shader(new_aov)
            try:
                aovs.AOVInterface().addAOV(new_aov)
            except:pass
            print "[OF] info: add aov ******%s****** successful" % new_aov
            pm.PyNode('aiAOV_%s.type' % new_aov).set(5)
            shader.outColor >> pm.PyNode('aiAOV_%s' % new_aov).defaultValue

        elif self.renderer == "mentalRay":
            if not aov_lists:
                self.add_mr_aov("mask00")
            else:
                self.add_mr_aov("mask%02d" % (sorted(aov_lists)[-1]+1))

    def add_rim_aov(self, *args):
        self.add_costom_aov("rim")
        shader = self.create_default_mask_aov_shader()
        shader.outColor >> pm.PyNode('aiAOV_rim').defaultValue
        print "[OF] info: add aov ******rim****** successful"
            
    def add_custom_aov(self, *args):
        if self.renderer == "arnold":
            st.newAOVPrompt()
        elif self.renderer == "mentalRay":
            result = pm.promptDialog(button=[u'创建', u'取消'],
                                        defaultButton='Create',
                                        message=u'mentalRay aov',
                                        title=u'创建aov')
            if result == u'创建':
                new_aov = pm.promptDialog(query=1, text=1)
                self.add_mr_aov(new_aov)

    def add_mr_aov(self, aov_name):
        if aov_name not in self.get_aov_name_lists():
            pm.createNode('renderPass', n=aov_name)
            pm.mel.eval('''applyAttrPreset "%s" "C:/Program Files/Autodesk/Maya2014/presets/attrPresets/renderPass/customColor.mel" 1;''' % aov_name)

    def rebuld_aov(self, *args):
        aov_mapping = dict([(i, self.MASK_PATTERN2.findall(i.name())[0])
            for i in pm.ls(type="writeToColorBuffer")
            if self.MASK_PATTERN2.findall(i.name())])
        from pprint import pprint
        pprint(aov_mapping)
        for i in aov_mapping.values():
            self.add_mr_aov(i)
        for i in aov_mapping:
            pm.PyNode(aov_mapping[i]).message >> i.renderPass

    def show_aov_lists(self, *args):
        self.pop[args[0]].deleteAllItems(1)
        for i in [j for j in self.get_aov_name_lists() if j.startswith("mask")
                  or j.startswith("rim") or j.startswith("hair") or j.startswith("all")]:
            pm.menuItem(parent=self.pop[args[0]], label=i,
                command=pm.Callback(self.connect_shader, i, args[0]))

    def get_aov_name_lists(self, *args):
        if self.renderer == "arnold":
            return [i.name for i in aovs.getAOVs()]
        elif self.renderer == "mentalRay":
            return [i.name() for i in pm.ls(type="renderPass")]

    def get_aov_index(self, sg_node, aov_name):
        #pm.select(sg_node, r=1, ne=1)
        #pm.mel.eval('showEditorExact "%s"' % (sg_node))
#        if set(self.get_aov_name_lists()) != set([i.aovName.get()
#            for i in sg_node.aiCustomAOVs if i.aovName.get()]):
#            print "%s need update its aov info." % (sg_node)
#            se.ShadingEngineTemplate("shadingEngine").updateAOVFrame(sg_node.aiCustomAOVs)
        aov_list = [i.aovName.get() for i in sg_node.aiCustomAOVs]
        # 2014.10.09 Yan-Chen Liao , Update Template
        if aov_name not in aov_list:
            se.ShadingEngineTemplate("shadingEngine").updateAOVFrame(sg_node.aiCustomAOVs)
            print '[updating shadingEngineTemplate]'
            aov_list = [i.aovName.get() for i in sg_node.aiCustomAOVs]
        return aov_list.index(aov_name)

    def get_object_list(self):
        selected_objects = []
        for i in pm.ls(sl=1):
            if i.type() in ['mesh', 'nurbsSurface', 'pgYetiMaya']:
                selected_objects.append(i)
            else:
                if i.type() == 'transform':
                    children = pm.ls(i, ap=1, dag=1, lf=1)
                    for child in children:
                        if child.type() in ['mesh', 'nurbsSurface', 'pgYetiMaya'] and not child.name().endswith('Orig'):
                            selected_objects.append(child)
        selected_objects = list(set(selected_objects))
        return selected_objects

    def get_sg_node_of_mesh(self, mesh):
        return mesh.outputs(type='shadingEngine')

    def get_sg_node_of_selected(self):
        sg_nodes = []
        all_meshes = self.get_object_list()
        if all_meshes:
            for mesh in all_meshes:
                sg_nodes.extend(self.get_sg_node_of_mesh(mesh))
        sg_nodes = list(set(sg_nodes))
        return sg_nodes

    def connect_shader(self, *args):
        #args(mask00, red)
        print 'args', args
        if not pm.checkBox('hair_check', q=1, value=1) and not pm.checkBox('all_check', q=1, value=1):
            if self.renderer == "arnold":
                sg_nodes = self.get_sg_node_of_selected()
                if sg_nodes:
                    shader = self.create_shader(args[1])
                    progress_dialog = QProgressDialog('<Total: %s>build aov...,Please wait......' % len(sg_nodes), 'Cancel', 0, len(sg_nodes))
                    progress_dialog.setWindowModality(Qt.WindowModal)
                    progress_dialog.show()
                    value = 0
                    for i in sg_nodes:
                        progress_dialog.setValue(value)
                        if progress_dialog.wasCanceled():
                            break
                        index = self.get_aov_index(i, args[0])
                        opacity_attr = self.get_opacity_attr(i)
                        if args[0] == 'rim':
                            shader.outColor >> i.aiCustomAOVs[index].aovInput
                            print '[connect shader] %s >> %s.%s' % (shader, i, args[0])
                            value += 1
                            continue
                        if not opacity_attr:
                            shader.outColor >> i.aiCustomAOVs[index].aovInput
                            print '[connect shader] %s >> %s.%s' % (shader, i, args[0])
                        else:
                            new_shader = self.create_new_shader(args[1])
                            try:
                                pm.connectAttr(opacity_attr, new_shader.opacity)
                            except:
                                try:
                                    pm.connectAttr(opacity_attr.node().outAlpha, new_shader.opacity)
                                except Exception as e:
                                    print e
                            aiStandard_shader = self.create_aistandard_shader()
                            new_shader.outColor >> aiStandard_shader.emissionColor
                            aiStandard_shader.aovEmission.set(args[0])
                            aiStandard_shader.outColor >> i.aiCustomAOVs[index].aovInput
                            print '[connect shader] %s >> %s.%s' % (aiStandard_shader, i, args[0])
                        value += 1
            elif self.renderer == "mentalRay":
                selects = []
                for i in pm.ls(sl=1, dag=1):
                    try:
                        if i.type() == "mesh" or i.type() == 'nurbsSurface':
                            selects.append(i)
                        elif i.getShape():
                            if i.getShape().type() == "mesh" or i.getShape().type() == 'nurbsSurface':
                                selects.append(i.getShape())
                    except:
                        pass
                selects = set([j for i in selects
                    for j in self.get_obj_shader(i)])
                print selects
                for i in selects:
                    for buffer in i.outputs(type="writeToColorBuffer"):
                        if buffer.name().startswith(args[0]):
                            pm.delete(buffer)
                    shader = self.create_mr_color_buffer(args)
                    try:
                        i.outColor >> shader.evaluationPassThrough
                    except:
                        try:
                            i.outValue >> shader.evaluationPassThrough
                        except:
                            try:
                                i.diffuse >> shader.evaluationPassThrough
                            except:
                                try:
                                    i.diffuse_color >> shader.evaluationPassThrough
                                except:
                                    try:
                                        i.base_color >> shader.evaluationPassThrough
                                    except:
                                        pass
                    # "Del unused" will delete mask node, connect mask back to shader's temp attr
                    attrname = 'of_pass_%s' % args[1]
                    if not i.hasAttr(attrname):
                        print i, attrname
                        i.addAttr(attrname, at='float')
                    shader.colorR >> pm.PyNode('%s.%s' % (i, attrname))
                    pm.PyNode(args[0]).message >> shader.renderPass

    #==================================hair aov===================================================#
        if pm.checkBox('hair_check', q=1, value=1):
            hairs = self.get_hairs_by_select()
            if hairs:
                for hair in hairs:
                    self.add_attribute(hair, args[0], args[1])
                    print '[add attribute] %s.mtoa_constant_%s' % (hair, args[0])
            else:
                QMessageBox.information(None, 'Information', 'Nothing Selected')

        if pm.checkBox('all_check', q=1, value=1):
            all_shapes = self.get_all_by_select()
            if all_shapes:
                for shape in all_shapes:
                    self.add_attribute(shape, args[0], args[1])
                    print '[add attribute] %s.mtoa_constant_%s' % (shape, args[0])
            else:
                QMessageBox.information(None, 'Information', 'Nothing Selected')

    def get_obj_shader(self, obj):
        return list(set(pm.ls([i.inputs() for i in obj.shadingGroups()], materials=1)))
#
#
#
#
#   Added by HeShuai <Add costom AOVs like AO, ambocc, lambert.......>

    def create_shader(self, color_name):
        if color_name == "rim":
            shader_name = "aiOf_aiRimFilter"
        else:
            shader_name = "aiUtility"
        if not pm.objExists(color_name+'_SHD'):
            shader = pm.shadingNode(shader_name, asShader=True, name=color_name+'_SHD')
        else:
            shader = pm.PyNode(color_name+'_SHD')
        if color_name == "rim":
            shader.Exp.set(6)
            shader.BaseColor.set([0, 0, 0])
        else:
            shader.color.set(self.pass_dict[color_name][1], type="double3")
            shader.shadeMode.set(2)
        return shader

    def create_new_shader(self, color_name):
        shader = pm.shadingNode('aiUtility', asShader=True, name=color_name+'_new_SHD')
        shader.color.set(self.pass_dict[color_name][1], type="double3")
        shader.shadeMode.set(2)
        return shader

    def create_aistandard_shader(self, emission_name='emission_aiStandard'):
        shader = pm.shadingNode('aiStandard', asShader=True, name=emission_name)
        shader.color.set(0, 0, 0)
        shader.Kd.set(0)
        shader.emission.set(1)
        return shader
        
    def get_opacity_attr(self, sg_node):
        shader = opacity_attr = None
        try:
            shader = pm.listConnections(sg_node.surfaceShader, source=1, destination=0)[0]
        except:pass
        if shader:
            try:
                opacity_attr = pm.listConnections(shader.opacity, source=1, destination=0, plugs=1)[0]
                opacity_attr = opacity_attr.node().outAlpha
            except:pass
        if opacity_attr:
            if opacity_attr.node().type() == 'file':
                opacity_attr.node().alphaIsLuminance.set(1)
            if opacity_attr.node().type() == 'remapHsv':
                opacity_attr = opacity_attr.node().outColorR
            if opacity_attr.node().type() == 'blendColors':
                opacity_attr = opacity_attr.node().outputR
        return opacity_attr

    def create_mr_color_buffer(self, args):
        shader = pm.createNode('writeToColorBuffer', n="_".join(args))
        shader.color.set(self.pass_dict[args[1]][1], type="double3")
        return shader
        
    ########add costom aov
    def add_costom_aov(self, name):
        if self.renderer == 'arnold':
            if not name in self.get_aov_name_lists():
                try:
                    aovs.AOVInterface().addAOV(name)
                except:pass
            pm.PyNode('aiAOV_%s.type' % name).set(5)
            pm.PyNode('aiAOV_%s.enabled' % name).set(1)

    def get_sg_node_of_opacity(self):
        sg_nodes_of_opacity = []
        for sg_node in pm.ls(type='shadingEngine'):
            if self.get_costom_opacity_attr(sg_node):
                sg_nodes_of_opacity.append(sg_node)
        return sg_nodes_of_opacity

    def get_costom_opacity_attr(self, sg_node):
        shader = opacity_attr = None
        try:
            shader = pm.listConnections(sg_node.surfaceShader, source=1, destination=0)[0]
        except:pass
        if shader:
            try:
                opacity_attr = pm.listConnections(shader.opacity, source=1, destination=0, plugs=1)[0]  
            except:pass
        return opacity_attr
        
    def create_costom_shader(self, name):
        if self.renderer == 'arnold':
            if name == 'AO':
                shader_type = 'aiAmbientOcclusion'
                shader_name = 'AO_aov_shader'
            if name == 'ambocc':
                shader_type = 'aiUtility'
                shader_name = 'ambocc_aov_shader'
            if name == 'lambert':
                shader_type = 'aiUtility'
                shader_name = 'lambert_aov_shader'
            if not pm.objExists(shader_name):
                shader = pm.shadingNode(shader_type, asShader=True, name=shader_name)
            else:
                shader = pm.PyNode(shader_name)
            if name == 'ambocc':
                shader.shadeMode.set(3)
            if name == 'lambert':
                shader.shadeMode.set(1)
            if name == 'rim':
                shader.Exp.set(6)
                shader.BaseColor.set([0, 0, 0])
            return shader
            
    def create_new_costom_shader(self, name): 
        if self.renderer == 'arnold':
            if name == 'AO':
                shader_type = 'aiAmbientOcclusion'
                shader_name = 'AO_aov_shader_new'
            if name == 'ambocc':
                shader_type = 'aiUtility'
                shader_name = 'ambocc_aov_shader_new'
            if name == 'lambert':
                shader_type = 'aiUtility'
                shader_name = 'lambert_aov_shader_new'
            shader = pm.shadingNode(shader_type, asShader=True, name=shader_name)
            if name == 'ambocc':
                shader.shadeMode.set(3)
            if name == 'lambert':
                shader.shadeMode.set(1)
            return shader

    def connect_default_shader(self, aov_name):
        shader = self.create_costom_shader(aov_name)
        shader.outColor >> pm.PyNode('aiAOV_%s' % aov_name).defaultValue
        print '[OF] info: %s\'s default shader has been connected' % aov_name
            
    def connect_costom_shader(self, name):
        sg_nodes = self.get_sg_node_of_opacity()
        if sg_nodes:
            progress_dialog = QProgressDialog('<Total: %s>build aov...,Please wait......' % len(sg_nodes), 'Cancel', 0, len(sg_nodes))
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            value = 0
            for i in sg_nodes:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                   break
                index = self.get_aov_index(i, name)
                opacity_attr = self.get_costom_opacity_attr(i)
                new_shader = self.create_new_costom_shader(name)
                try:
                    pm.connectAttr(opacity_attr, new_shader.opacity)
                except:
                    try:
                        pm.connectAttr(opacity_attr.node().outAlpha, new_shader.opacity)
                    except Exception as e:
                        print e
                aiStandard_shader = self.create_aistandard_shader(emission_name=name+'_emission_shader')
                new_shader.outColor >> aiStandard_shader.emissionColor
                aiStandard_shader.aovEmission.set(name)
                aiStandard_shader.outColor >> i.aiCustomAOVs[index].aovInput
                print '[connect shader] %s >> %s.%s' % (aiStandard_shader, i, name)
                value += 1
                
    def create_costom_aov(self, name):
        if self.renderer == 'arnold':
            start = time.time()
            self.add_costom_aov(name)
            self.connect_default_shader(name)
            if name != 'rim':
                self.connect_costom_shader(name)
            print "%s cost %s(s)" % (name, time.time()-start)

    ########set attributes
    def set_ao_samples(self, *args):
        sample_value = 3
        try:
            sample_value = pm.PyNode('AO_aov_shader').samples.get()
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

#=================================================hair================================================================#
    def get_hairs_by_select(self):
        selected_objects = []
        if pm.ls(sl=1):
            for i in pm.ls(sl=1):
                if i.type() in ['pfxHair', 'pgYetiMaya', 'shaveHair']:
                    selected_objects.append(i)
                else:
                    if i.type() == 'transform':
                        children = pm.ls(i, ap=1, dag=1, lf=1)
                        for child in children:
                            if child.type() in ['pfxHair', 'pgYetiMaya', 'shaveHair']:
                                selected_objects.append(child)
        return selected_objects

    def get_all_by_select(self):
        selected_objects = []
        if pm.ls(sl=1):
            for i in pm.ls(sl=1):
                if i.type() in ['pfxHair', 'pgYetiMaya', 'shaveHair', 'mesh', 'nurbsSurface']:
                    selected_objects.append(i)
                else:
                    if i.type() == 'transform':
                        children = pm.ls(i, ap=1, dag=1, lf=1)
                        for child in children:
                            if child.type() in ['pfxHair', 'pgYetiMaya', 'shaveHair', 'pgYetiGroom', 'mesh', 'nurbsSurface']:
                                selected_objects.append(child)
        return selected_objects

    def create_aiWriteColor_node(self, name, color):
        ai_write_node = pm.shadingNode('aiWriteColor', name=name+'_aov_aiWrite_color', asShader=1)
        ai_write_node.input.set(self.pass_dict[color][1])
        ai_write_node.aov_name.set(name)
        return ai_write_node

            
def aov_settings():
    ObjectRenderPass()


if __name__ == '__main__':
    ObjectRenderPass()