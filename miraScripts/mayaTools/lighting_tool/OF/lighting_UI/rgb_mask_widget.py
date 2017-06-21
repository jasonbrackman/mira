import pymel.core as pm
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import os
from get_parent_dir import get_parent_dir
import time
import functools
import public_ctrls


color_dict = {'red': ['R_ID', (1, 0, 0), '#FF0000'],
              'green': ['G_ID', (0, 1, 0), '#00FF00'],
              'blue': ['B_ID', (0, 0, 1), '#0000FF'],
              'cyan': ['A_ID', (0, 1, 1), '#00FFFF'],
              'yellow': ['Y_ID', (1, 1, 0), '#FFFF00'],
              'magenta': ['M_ID', (1, 0, 1), '#FF00FF'],
              'orange': ['O_ID', (1, 0.647, 0), '#FFA500'],
              'purple': ['P_ID', (0.5, 0, 0.5), '#800080'],
              'matte':['Matte', (0, 0, 0), '#000000']}


def undo(func):
    def _undo(*args, **kwargs):
        try:
            mc.undoInfo(ock=1)
            result = func(*args, **kwargs)
        except Exception, e:
            raise e
        else:
            return result
        finally:
            mc.undoInfo(cck=1)
    return _undo
    

def get_current_renderer():
    current_renderer = pm.PyNode('defaultRenderGlobals').currentRenderer.get()
    return current_renderer


def get_object_list():
    selected_objects = []
    for i in pm.ls(sl=1):
        if i.type() in ['mesh', 'nurbsSurface']:
            selected_objects.append(i)
        else:
            if i.type() == 'transform':
                children = pm.ls(i, ap=1, dag=1, lf=1)
                for child in children:
                    if child.type() in ['mesh', 'nurbsSurface']:
                        selected_objects.append(child)
    selected_objects = list(set(selected_objects))
    return selected_objects
    
    
def get_sg_node_of_mesh(mesh):
    sg_nodes = mesh.outputs(type='shadingEngine')
    sg_nodes = list(set(sg_nodes))
    return sg_nodes
    

def get_sg_node_of_selected():
    sg_nodes = []
    all_meshes = get_object_list()
    if all_meshes:
        for mesh in all_meshes:
            sg_nodes.extend(get_sg_node_of_mesh(mesh))
    sg_nodes = list(set(sg_nodes))
    return all_meshes, sg_nodes
    
    
def get_displacement_attr_of_sg(sg_node):
    displacement_attr = pm.listConnections(sg_node.displacementShader, source=1, destination=0, plugs=1)
    if displacement_attr:
        return displacement_attr[0]
    else:
        return None
        
        
def get_shader_of_sg(sg_node):
    shader = pm.listConnections(sg_node.surfaceShader, source=1, destination=0)
    if not shader:
        try:
            shader = pm.listConnections(sg_node.miMaterialShader, source=1, destination=0)
        except:pass
    if shader:
        return shader[0]
    else:
        return None
        
        
def get_opacity_attr_of_shader(shader):
    opacity_attr = None
    try:
        opacity_attr = pm.listConnections(shader.opacity, source=1, destination=0, plugs=1)[0]
    except:
        try:
            opacity_attr = pm.listConnections(shader.transparency, source=1, destination=0, plugs=1)[0]
        except:
            try:
                opacity_attr = pm.listConnections(shader.outTransparency, source=1, destination=0, plugs=1)[0]
            except:
                try:
                    opacity_attr = pm.listConnections(shader.cutout_opacity, source=1, destination=0, plugs=1)[0]
                except:pass
    return opacity_attr

    
def get_meshes_of_sg_node(sg_node):
    transforms = [i for i in sg_node.inputs() if i.type() == 'transform']
    if len(transforms) > 5000:
        return 0, transforms
    else:
        meshes = [j for t in transforms for j in pm.ls(t, ap=1, dag=1, lf=1) if j.type() in ['mesh', 'nurbsSurface']]
        return 1, list(set(meshes))

    
def get_my_list(sg_node, all_mehses):
    displacement_attr = get_displacement_attr_of_sg(sg_node)
    shader = get_shader_of_sg(sg_node)
    opacity_attr = get_opacity_attr_of_shader(shader)
    meshes_list = get_meshes_of_sg_node(sg_node)
    if not meshes_list[0]:
        meshes = meshes_list[1]
    else:
        meshes = list(set(meshes_list[1]) & set(all_mehses))
    return sg_node, displacement_attr, opacity_attr, meshes
    
    
def create_mask_shader(r, g, b, a, shader_name):
    if not pm.objExists(shader_name):
        shader = pm.shadingNode('surfaceShader', asShader=1, name=shader_name)
        shader.outColor.set(r, g, b)
        shader.outMatteOpacity.set(a, a, a)
    else:
        shader = pm.PyNode(shader_name)
    if not pm.objExists(shader_name+'_SG'):
        sg = pm.sets(noSurfaceShader=1, renderable=1, empty=1, name=shader_name+'_SG')
        shader.outColor >> sg.surfaceShader
    else:
        sg = pm.PyNode(shader_name+'_SG')
    pm.select(clear=1)
    return shader, sg
    
    
def create_new_sg_node():
    sg = pm.sets(noSurfaceShader=1, renderable=1, empty=1, name='mask_sg_hs')
    return sg
    

def create_new_mask_shader(r, g, b, a):
    shader = pm.shadingNode('surfaceShader', asShader=1, name='mask_shader_hs')
    shader.outColor.set(r, g, b)
    shader.outMatteOpacity.set(a, a, a)
    return shader

    
def create_reverse():
    node = pm.shadingNode('reverse', asUtility=1, name='mask_reverse_hs')
    return node
########shadows


def create_shadow_shader():
    current_renderer = get_current_renderer()
    if current_renderer == 'arnold':
        shadow_node = create_shadow_shader_arnold()
    if current_renderer == 'mentalRay':
        shadow_node = create_shadow_shader_mentalray()
    return shadow_node


def create_shadow_shader_arnold():
    if not pm.objExists('shadow_shader_hs_arnold'):
        shadow_shader = pm.shadingNode('aiUtility', asShader=1, name='shadow_shader_hs_arnold')
        shadow_shader.shadeMode.set(1)
    else:
        shadow_shader = pm.PyNode('shadow_shader_hs_arnold')
    if not pm.objExists('shadow_catcher_hs_arnold'):
        shadow_catcher = pm.shadingNode('aiShadowCatcher', asShader=1, name='shadow_catcher_hs_arnold')
        shadow_catcher.enableTransparency.set(1)
        shadow_shader.outColor >> shadow_catcher.shadowTransparency
    else:
        shadow_catcher = pm.PyNode('shadow_catcher_hs_arnold')
    if not pm.objExists('shadow_SG_hs_arnold'):
        shadow_sg = pm.sets(renderable=1, noSurfaceShader=1, empty=1, name='shadow_SG_hs_arnold')
        shadow_catcher.outColor >> shadow_sg.surfaceShader
    else:
        shadow_sg = pm.PyNode('shadow_SG_hs_arnold')
    pm.select(clear=1)
    return shadow_catcher, shadow_sg


def create_shadow_shader_mentalray():
    if not pm.objExists('shadow_SG_hs_mentalray'):
        shadow_shader = pm.shadingNode('useBackground', asShader=1, name='shadow_shader_hs_mentalray')
        shadow_sg = pm.sets(renderable=1, noSurfaceShader=1, empty=1, name='shadow_SG_hs_mentalray')
        shadow_shader.specularColor.set(0, 0, 0)
        shadow_shader.reflectivity.set(0)
        shadow_shader.reflectionLimit.set(0)
        shadow_shader.outColor >> shadow_sg.surfaceShader
        return [shadow_shader, shadow_sg]
    else:
        return [pm.PyNode('shadow_shader_hs_mentalray'), pm.PyNode('shadow_SG_hs_mentalray')]


def create_new_shadow_shader():
    current_renderer = get_current_renderer()
    if current_renderer == 'arnold':
        shadow_shader = create_shadow_shader_arnold()[0]
    if current_renderer == 'mentalRay':
        shadow_shader = create_new_mentalray_shadow_shader()
    return shadow_shader


def create_new_mentalray_shadow_shader():
    shadow_shader = pm.shadingNode('useBackground', asShader=1, name='new_shadow_shader')
    shadow_shader.specularColor.set(0, 0, 0)
    shadow_shader.reflectivity.set(0)
    shadow_shader.reflectionLimit.set(0)
    return shadow_shader


def create_new_shadow_sg():
    sg = pm.sets(noSurfaceShader=1, renderable=1, empty=1, name='shadow_sg_hs')
    return sg


class RGBMaskWidget(QDialog):
    def __init__(self, parent=None):
        super(RGBMaskWidget, self).__init__(parent)
        self.parent_dir = get_parent_dir()
        current_renderer = get_current_renderer()
        self.setWindowTitle('mask')
        self.setObjectName('mask')
        self.resize(500, 40)
        rgb_layout = QHBoxLayout(self)
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        rgb_layout.addWidget(frame)
        main_layout = QVBoxLayout(frame)
        up_layout = QHBoxLayout()
        self.info_label = QLabel()
        self.info_label.setText('current renderer: <font color="#00FF00" size=4><b>%s</b> </font>' % current_renderer)
        self.set_matte_check = QCheckBox('Alpha')
        self.set_matte_check.setStyleSheet('QCheckBox::indicator:unchecked{border: 1px solid #555555;}')
        up_layout.addWidget(self.info_label)
        up_layout.addStretch()
        up_layout.addWidget(self.set_matte_check)
        button_layout = QGridLayout()
        i = j =0
        colors = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta', 'orange', 'purple', 'matte']
        for btn in colors:
            self.color_btn = QPushButton(color_dict[btn][0])
            self.color_btn.setStyleSheet('QPushButton{background:%s}' % color_dict[btn][2])
            self.color_btn.clicked.connect(functools.partial(self.assign_mask, color_dict[btn][0], *color_dict[btn][1]))
            button_layout.addWidget(self.color_btn, i, j)
            j += 1
            if j == 5:
                i += 1
                j = 0
        self.shadow_btn = QPushButton('Shadow')
        self.shadow_btn.setStyleSheet('QPushButton{background:#AAAAAA}')
        button_layout.addWidget(self.shadow_btn, i, j)
        main_layout.addLayout(up_layout)
        main_layout.addLayout(button_layout)
        self.set_background()
        self.set_signals()

    def set_background(self):
        image_path = os.path.join(self.parent_dir, 'icons', 'background_icons', 'tx.png')
        self.image = QImage(image_path)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.image.scaled(event.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def set_signals(self):
        self.shadow_btn.clicked.connect(self.assign_shadow)
    
    @undo
    def assign_mask(self, name, r, g, b, *args):
        start = time.time()
        current_renderer = get_current_renderer()
        all_meshes, sg_nodes = get_sg_node_of_selected()
        print "get meshes & sg nodes successful"
        if all_meshes:
            if self.set_matte_check.isChecked():
                node = create_mask_shader(r, g, b, 1, name+'_X')
            else:
                node = create_mask_shader(r, g, b, 0, name)
            progress_dialog = QProgressDialog('Assign materials,Please wait......', 'Cancel', 0, len(sg_nodes))
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            value = 0
            for sg_node in sg_nodes:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                    break
                my_list = get_my_list(sg_node, all_meshes)
                #sg, dis, opacity, meshes
                if my_list[3]:
                    if not my_list[2]:
                        ########no displacement, no opacity
                        if not my_list[1]:
                            pm.sets(node[1], fe=my_list[3])
                        ########displacement , no opacity
                        else:
                            if 'mask_sg_hs' in my_list[0].name():
                                node[0].outColor >> my_list[0].surfaceShader
                            else:
                                dis_sg_node = create_new_sg_node()
                                pm.connectAttr(node[0].outColor, dis_sg_node.surfaceShader, force=1)
                                pm.connectAttr(my_list[1], dis_sg_node.displacementShader)
                                pm.sets(dis_sg_node, fe=my_list[3])
                    ########no displacement, opacity        
                    else:
                        dis_sg_node = create_new_sg_node()
                        if self.set_matte_check.isChecked():
                            mask_shader = create_new_mask_shader(r, g, b, 1)
                        else:
                            mask_shader = create_new_mask_shader(r, g, b, 0)
                        mask_shader.outColor >> dis_sg_node.surfaceShader
                        if my_list[1]:
                            pm.connectAttr(my_list[1], dis_sg_node.displacementShader)
                        if current_renderer == 'mentalRay':
                            try:
                                pm.connectAttr(my_list[2], mask_shader.outTransparency)
                            except:
                                try:
                                    pm.connectAttr(my_list[2].node().outTransparency, mask_shader.outTransparency)
                                except:pass
                        if current_renderer == 'arnold':
                            if my_list[2].node().name().startswith('mask_reverse_hs'):
                                pm.connectAttr(my_list[2], mask_shader.outTransparency)
                            else:
                                reverse_node = create_reverse()
                                pm.connectAttr(my_list[2], reverse_node.input)
                                reverse_node.output >> mask_shader.outTransparency
                        pm.sets(dis_sg_node, fe=my_list[3])
                value += 1
                mc.select(all_meshes, r=1)
            print time.time()-start
            
    @undo
    def assign_shadow(self, *args):
        all_meshes, sg_nodes = get_sg_node_of_selected()
        if all_meshes:
            node = create_shadow_shader()
            progress_dialog = QProgressDialog('<Total:%s>Assign materials,Please wait......' % len(sg_nodes), 'Cancel', 0, len(sg_nodes))
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            value = 0
            for sg_node in sg_nodes:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                    break
                my_list = get_my_list(sg_node, all_meshes)
                if 'shadow_sg_hs' in my_list[0].name():
                    value += 1
                    continue
                if my_list[3]:
                    if not my_list[2]:
                        ########no displacement, no opacity
                        if not my_list[1]:
                            pm.sets(node[1], fe=my_list[3])
                        else:
                            dis_sg_node = create_new_shadow_sg()
                            node[0].outColor >> dis_sg_node.surfaceShader
                            pm.connectAttr(my_list[1], dis_sg_node.displacementShader)
                            pm.sets(dis_sg_node, fe=my_list[3])
                    else:
                        my_list[2].node().alphaIsLuminance.set(1)
                        shadow_shader = create_new_shadow_shader()
                        sg_node = create_new_shadow_sg()
                        shadow_shader.outColor >> sg_node.surfaceShader
                        if my_list[1]:
                            pm.connectAttr(my_list[1], sg_node.displacementShader)
                        try:
                            pm.connectAttr(my_list[2].node().outAlpha, shadow_shader.matteOpacity, force=1)
                        except:pass
                        pm.sets(sg_node, fe=my_list[3])
                value += 1
                mc.select(all_meshes, r=1)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()

    @classmethod
    def show_ui(cls):
        if mc.window('mask', q=1, exists=1):
            mc.deleteUI('mask')
        nw = cls(public_ctrls.get_maya_win())
        nw.show()


def run():
    current_renderer = get_current_renderer()
    if current_renderer not in ['mentalRay', 'arnold']:
        QMessageBox.information(None, 'Tip', 'Current renderer is not arnold or mentalray')
        return
    RGBMaskWidget.show_ui()
        
        
if __name__ == '__main__':
    run()