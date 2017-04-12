import logging
import pymel.core as pm
import maya.cmds as mc
import maya.mel as mel


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


def delete_unused_nodes():
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')


def create_surface_shader():
    node = pm.shadingNode("surfaceShader", asShader=1)
    return node
    

@undo
def convert_lambert_to_surface():
    selected_shaders = pm.ls(sl=1)
    if not selected_shaders:
        return
    for shader in selected_shaders:
        if shader.type() not in ["lambert", "blinn"]:
            continue
        # create surface shader
        surface_shader = create_surface_shader()
        # get .color source connection
        color_src_connection = shader.color.inputs(p=1)
        transparency_src_connection = shader.transparency.inputs(p=1)
        glow_src_connection = shader.incandescence.inputs(p=1)
        # if has connection connect to surface shader 
        if color_src_connection:
            color_src_connection[0] >> surface_shader.outColor
        else:
            color_value = shader.color.get()
            surface_shader.outColor.set(color_value)
            
        if transparency_src_connection:
            transparency_src_connection[0] >> surface_shader.outTransparency
        else:
            transparency_value = shader.transparency.get()
            surface_shader.outTransparency.set(transparency_value)
            
        if glow_src_connection:
            glow_src_connection[0] >> surface_shader.outGlowColor
        else:
            glow_value = shader.incandescence.get()
            surface_shader.outGlowColor.set(glow_value)
            
        # get sg node
        sg_node_connection = shader.outputs(type="shadingEngine", p=1)
        if sg_node_connection:
            surface_shader.outColor >> sg_node_connection[0]
        logging.info("Convert %s >> %s" % (shader, surface_shader))
    # delete unused nodes
    delete_unused_nodes()
    
    
if __name__ == "__main__":
    convert_lambert_to_surface()
