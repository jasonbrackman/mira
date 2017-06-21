__author__ = 'heshuai'
import  pymel.core as pm
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import time


########current_renderlayer must be type string
def get_meshes_in_layer(current_renderlayer):
    meshes_in_layer = []
    transforms = [i for i in pm.PyNode(current_renderlayer).connections() if i.type() == 'transform']
    transforms = list(set(transforms))
    for i in transforms:
        for j in pm.ls(i, ap=1, dag=1, lf=1):
            try:
                if j.type() in ['mesh', 'nurbsSurface']:
                    meshes_in_layer.append(j)
            except:pass
    meshes_in_layer = list(set(meshes_in_layer))
    return meshes_in_layer


def get_sg_node_of_mesh(mesh):
    return mesh.outputs(type='shadingEngine')
    

def get_all_sg_node_in_layer(all_meshes):
    sg_nodes = []
    if all_meshes:
        for mesh in all_meshes:
            sg_nodes.extend(get_sg_node_of_mesh(mesh))
    sg_nodes = list(set(sg_nodes))
    return sg_nodes
    
    
def get_displacement_attr_of_sg(sg_node):
    displacement_attr = pm.listConnections(sg_node.displacementShader, source=1, destination=0, plugs=1)
    if displacement_attr:
        return displacement_attr[0]
    else:
        return None
    
    
def get_shader_of_sg(sg_node):
    shader = pm.listConnections(sg_node.surfaceShader, source=1, destination=0)
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
    meshes = []
    transforms = [i for i in sg_node.inputs() if i.type() == 'transform']
    if len(transforms) > 100:
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
    
    
def create_ao_shader():
    ao_shader = pm.shadingNode('aiAmbientOcclusion', asShader=1, name='AO_shader')
    sg = pm.sets(noSurfaceShader=1, renderable=1, empty=1, name='AO_SG')
    pm.connectAttr(ao_shader.outColor, sg.surfaceShader, force=1)
    return [ao_shader, sg]
    

def main():
    current_layer = pm.editRenderLayerGlobals(currentRenderLayer=1, q=1)
    all_meshes = get_meshes_in_layer(current_layer)
    if all_meshes:
        sg_nodes = get_all_sg_node_in_layer(all_meshes)
        if not pm.objExists('AO_SG'):    
            ao_sg_node = create_ao_shader()[1]
        else:
            ao_sg_node = pm.PyNode('AO_SG')
        progress_dialog = QProgressDialog('<Total:%s>Assign materials,Please wait......' % len(sg_nodes), 'Cancel', 0, len(sg_nodes))
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()
        value = 0
        start = time.time()
        for sg_node in sg_nodes:
            progress_dialog.setValue(value)
            if progress_dialog.wasCanceled():
                break
            my_list = get_my_list(sg_node, all_meshes)
            #sg_node, dis_attr, opacity_attr, meshes
            try:
                if my_list[3]:
                    if 'AO_SG' in my_list[0].name():
                        value += 1
                        continue
                    #no dis, no opacity
                    if not my_list[1] and not my_list[2]:
                        pm.sets(ao_sg_node, fe=my_list[3])
                    #dis, no opacity
                    elif my_list[1] and not my_list[2]:
                        dis_sg_node = pm.sets(noSurfaceShader=1, renderable=1, empty=1, name='AO_SG_dis')
                        pm.connectAttr(pm.PyNode('AO_shader').outColor, dis_sg_node.surfaceShader, force=1)
                        pm.connectAttr(my_list[1], dis_sg_node.displacementShader)
                        pm.sets(dis_sg_node, fe=my_list[3])
                    #no dis, opacity
                    elif not my_list[1] and my_list[2]:
                        shader, opacity_sg_node = create_ao_shader()
                        pm.connectAttr(my_list[2], shader.opacity)
                        pm.sets(opacity_sg_node, fe=my_list[3])
                    #dis, opacity
                    elif my_list[1] and my_list[2]:
                        shader, dis_sg_node = create_ao_shader()
                        pm.connectAttr(my_list[2], shader.opacity)
                        pm.connectAttr(my_list[1], dis_sg_node.displacementShader)
                        pm.sets(dis_sg_node, fe=my_list[3])
            except Exception as e:
                print e
            value += 1
        print 'AO cast %s(s)' % str(time.time()-start)
                

if __name__ == '__main__':
    main()