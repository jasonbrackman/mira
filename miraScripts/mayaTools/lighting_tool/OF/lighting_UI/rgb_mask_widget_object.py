import pymel.core as pm
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import public_ctrls
import os
from get_parent_dir import get_parent_dir


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
                children = pm.ls(i, dag=1, ap=1, lf=1)
                for child in children:
                    if child.type() in ['mesh', 'nurbsSurface']:
                        selected_objects.append(child)
    selected_objects = list(set(selected_objects))
    return selected_objects
    
    
def get_sg_node_of_mesh(mesh):
    sg_nodes = mesh.outputs(type='shadingEngine')
    sg_nodes = list(set(sg_nodes))
    if sg_nodes:
        if len(sg_nodes) == 1:
            return sg_nodes[0]
        elif len(sg_nodes) > 1:
            mask_sgs = list()
            for sg_node in sg_nodes:
                if 'mask_sg_hs' in sg_node.name():
                    mask_sgs.append(sg_node)
            sg_nodes = list(set(sg_nodes)-set(mask_sgs))
            if sg_nodes:
                return sg_nodes[0]
            else:
                return
    else:
        return
    
    
def get_displacement_attr_of_sg(sg_node):
    displacement_attr = pm.listConnections(sg_node.displacementShader, source=1, destination=0, plugs=1)
    if displacement_attr:
        return displacement_attr[0]
    else:
        return 
        
        
def get_shader_of_sg(sg_node):
    shader = pm.listConnections(sg_node.surfaceShader, source=1, destination=0)
    if not shader:
        try:
            shader = pm.listConnections(sg_node.miMaterialShader, source=1, destination=0)
        except:pass
    if shader:
        return shader[0]
    else:
        return 
        
        
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
    

def get_my_list(mesh):
    sg_node = get_sg_node_of_mesh(mesh)
    if sg_node:
        displacement_attr = get_displacement_attr_of_sg(sg_node)
        shader = get_shader_of_sg(sg_node)
        opacity_attr = get_opacity_attr_of_shader(shader)
        return shader, sg_node, displacement_attr, opacity_attr
    else:
        return None, None, None, None
    
    
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
    if not pm.objExists('shadow_sg_hs_arnold'):
        shadow_sg = pm.sets(renderable=1, noSurfaceShader=1, empty=1, name='shadow_sg_hs_arnold')
        shadow_catcher.outColor >> shadow_sg.surfaceShader
    else:
        shadow_sg = pm.PyNode('shadow_sg_hs_arnold')
    pm.select(clear=1)
    return [shadow_catcher, shadow_sg]


def create_shadow_shader_mentalray():
    if not pm.objExists('shadow_sg_hs_mentalray'):
        shadow_shader = pm.shadingNode('useBackground', asShader=1, name='shadow_shader_hs_mentalray')
        shadow_sg = pm.sets(renderable=1, noSurfaceShader=1, empty=1, name='shadow_sg_hs_mentalray')
        shadow_shader.specularColor.set(0, 0, 0)
        shadow_shader.reflectivity.set(0)
        shadow_shader.reflectionLimit.set(0)
        shadow_shader.outColor >> shadow_sg.surfaceShader
        return shadow_shader, shadow_sg
    else:
        return pm.PyNode('shadow_shader_hs_mentalray'), pm.PyNode('shadow_sg_hs_mentalray')


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
        y_pos = public_ctrls.get_maya_main_win_pos()[1] + (public_ctrls.get_maya_main_win_size()[1])/4
        self.move(public_ctrls.get_maya_main_win_pos()[0], y_pos)
        self.setWindowTitle('mask')
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinimizeButtonHint)
        self.resize(500, 40)
        rgb_layout = QHBoxLayout(self)
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        rgb_layout.addWidget(frame)
        main_layout = QVBoxLayout(frame)
        self.info_label = QLabel()
        button_layout = QHBoxLayout()
        #button_layout.setSpacing(0)
        #button_layout.setContentsMargins(0, 0, 0, 0)
        self.red_mask_btn = QPushButton('R_ID')
        self.red_mask_btn.setStyleSheet('QPushButton{background:#FF0000}')
        self.green_mask_btn = QPushButton('G_ID')
        self.green_mask_btn.setStyleSheet('QPushButton{background:#00FF00}')
        self.blue_mask_btn = QPushButton('B_ID')
        self.blue_mask_btn.setStyleSheet('QPushButton{background:#0000FF}')
        self.black_mask_btn = QPushButton('Matte')
        self.black_mask_btn.setStyleSheet('QPushButton{background:#000000}')
        self.shadow_btn = QPushButton('Shadow')
        self.shadow_btn.setStyleSheet('QPushButton{background:#AAAAAA}')
        button_layout.addWidget(self.red_mask_btn)
        button_layout.addWidget(self.green_mask_btn)
        button_layout.addWidget(self.blue_mask_btn)
        button_layout.addWidget(self.black_mask_btn)
        button_layout.addWidget(self.shadow_btn)
        self.set_matte_check = QCheckBox('Alpha')
        self.set_matte_check.setStyleSheet('QCheckBox::indicator:unchecked{border: 1px solid #555555;}')
        main_layout.addWidget(self.info_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.set_matte_check)
        self.set_label_text()
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

    def set_label_text(self):
        current_renderer = get_current_renderer()
        if current_renderer in ['mentalRay', 'arnold']:
            self.info_label.setText('current renderer: <font color="#00FF00" size=4><b>%s</b> </font>' % current_renderer)
        else:
            self.info_label.setText('current renderer: <font color="#FF0000" size=4><b>%s</b> </font>' % current_renderer)
            self.shadow_btn.setEnabled(False)
            self.red_mask_btn.setEnabled(False)
            self.green_mask_btn.setEnabled(False)
            self.blue_mask_btn.setEnabled(False)
            self.black_mask_btn.setEnabled(False)

    def set_signals(self):
        self.red_mask_btn.clicked.connect(self.assign_red_mask)
        self.green_mask_btn.clicked.connect(self.assign_green_mask)
        self.blue_mask_btn.clicked.connect(self.assign_blue_mask)
        self.black_mask_btn.clicked.connect(self.assign_black_mask)
        self.shadow_btn.clicked.connect(self.assign_shadow)

    def assign_red_mask(self):
        self.set_label_text()
        self.assign_mask(1, 0, 0, 'R_ID')

    def assign_green_mask(self):
        self.set_label_text()
        self.assign_mask(0, 1, 0, 'G_ID')

    def assign_blue_mask(self):
        self.set_label_text()
        self.assign_mask(0, 0, 1, 'B_ID')

    def assign_black_mask(self):
        self.set_label_text()
        self.assign_mask(0, 0, 0, 'Matte')
        
    @undo
    def assign_mask(self, r, g, b, name):
        current_renderer = get_current_renderer()
        all_meshes = get_object_list()
        if all_meshes:
            if self.set_matte_check.isChecked():
                node = create_mask_shader(r, g, b, 1, name+'_X')
                alpha = 1
            else:
                node = create_mask_shader(r, g, b, 0, name)
                alpha = 0
            progress_dialog = QProgressDialog('Assign materials,Please wait......', 'Cancel', 0, len(all_meshes))
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            value = 0
            for mesh in all_meshes:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                    break
                my_list = get_my_list(mesh)
                #my_list = shader, sg, dis, opacity
                print my_list
                if not my_list[1]:
                    pm.sets(node[1], fe=mesh)
                    continue
                if my_list[0]:
                    if 'mask_shader_hs' in my_list[0].name():
                        my_list[0].outColor.set(r, g, b)
                        my_list[0].outMatteOpacity.set(alpha, alpha, alpha)
                        value += 1
                        continue
                if not my_list[3]:
                    ########no displacement, no opacity
                    if not my_list[2]:
                        pm.sets(node[1], fe=mesh)
                    ########displacement , no opacity
                    else:
                        if 'mask_sg_hs' in my_list[1].name():
                            node[0].outColor >> my_list[1].surfaceShader
                        else:
                            dis_sg_node = create_new_sg_node()
                            node[0].outColor >> dis_sg_node.surfaceShader
                            pm.connectAttr(my_list[2], dis_sg_node.displacementShader)
                            pm.sets(dis_sg_node, fe=mesh)
                ########no displacement, opacity
                else:
                    dis_sg_node = create_new_sg_node()
                    if self.set_matte_check.isChecked():
                        mask_shader = create_new_mask_shader(r, g, b, 1)
                    else:
                        mask_shader = create_new_mask_shader(r, g, b, 0)
                    mask_shader.outColor >> dis_sg_node.surfaceShader
                    if my_list[2]:
                        pm.connectAttr(my_list[2], dis_sg_node.displacementShader)
                    if current_renderer == 'mentalRay':
                        try:
                            pm.connectAttr(my_list[3], mask_shader.outTransparency)
                        except:
                            try:
                                pm.connectAttr(my_list[3].node().outTransparency, mask_shader.outTransparency)
                            except:pass
                    if current_renderer == 'arnold':
                        if my_list[3].node().name().startswith('mask_reverse_hs'):
                            pm.connectAttr(my_list[3], mask_shader.outTransparency)
                        else:
                            reverse_node = create_reverse()
                            pm.connectAttr(my_list[3], reverse_node.input)
                            reverse_node.output >> mask_shader.outTransparency
                    pm.sets(dis_sg_node, fe=mesh)
            value += 1
    
    @undo
    def assign_shadow(self):
        self.set_label_text()
        all_meshes = get_object_list()
        if all_meshes:
            node = create_shadow_shader()
            progress_dialog = QProgressDialog('<Total:%s>Assign materials,Please wait......' % len(all_meshes), 'Cancel', 0, len(all_meshes))
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            value = 0
            for mesh in all_meshes:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                    break
                my_list = get_my_list(mesh)
                print my_list
                if 'shadow_sg_hs' in my_list[1].name():
                    value += 1
                    continue
                if not my_list[3]:
                    ########no displacement, no opacity
                    if not my_list[2]:
                        pm.sets(node[1], fe=mesh)
                    else:
                        dis_sg_node = create_new_shadow_sg()
                        node[0].outColor >> dis_sg_node.surfaceShader
                        pm.connectAttr(my_list[2], dis_sg_node.displacementShader)
                        pm.sets(dis_sg_node, fe=mesh)
                else:
                    my_list[3].node().alphaIsLuminance.set(1)
                    shadow_shader = create_new_shadow_shader()
                    sg_node = create_new_shadow_sg()
                    shadow_shader.outColor >> sg_node.surfaceShader
                    if my_list[2]:
                        pm.connectAttr(my_list[2], sg_node.displacementShader)
                    try:
                        pm.connectAttr(my_list[3].node().outAlpha, shadow_shader.matteOpacity, force=1)
                    except:pass
                    pm.sets(sg_node, fe=mesh)
            value += 1

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()


def run():
    global mw
    try:
        mw.close()
        mw.deleteLater()
    except:pass
    mw = RGBMaskWidget(public_ctrls.get_maya_win())
    mw.show()
        
        
if __name__ == '__main__':
    run()