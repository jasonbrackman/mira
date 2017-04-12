# coding = utf8
# __author__ = "heshuai"
# description="""  """


import re
import pymel.core as pm
import maya.cmds as mc
import mtoa.ui.ae.shadingEngineTemplate as se
import mtoa.ui.ae.shaderTemplate as st
import mtoa.aovs as aovs


def rebuild_arnold_aov():
    aov_lists = list()
    sg_nodes = pm.ls(type='shadingEngine')
    if len(sg_nodes) > 200:
        sg_nodes = sg_nodes[:200]
    for se in sg_nodes:
        for aov in se.aiCustomAOVs:
            print '[OF] Info:find', aov, aov.aovName.get()
            aov_lists.append(aov.aovName.get())
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
    aov_lists = list(set(aov_lists))
    for aov in aov_lists:
        if aov and aov not in get_aov_name_lists():
            try:
                aovs.AOVInterface().addAOV(aov)
                print '[OF] Info: Rebuild %s' % aov
            except:pass
                
                
def get_aov_name_lists():
    return [i.name for i in aovs.getAOVs()]
    
    
def get_all_meshes():
    return pm.ls(type='mesh')
    
    
def add_attribute(name):
    for mesh in get_all_meshes():
        if not hasattr(mesh, 'mtoa_constant_'+name):
            pm.addAttr(mesh, ln='mtoa_constant_'+name, dt='string')
            pm.setAttr(pm.PyNode('%s.mtoa_constant_%s' % (mesh, name), e=1, keyable=1))
            
            
def get_color_texture(mesh):
    try:
        sg_node = mesh.outputs(type='shadingEngine')[0]
        shader = pm.listConnections(sg_node.surfaceShader, source=1, destination=0)[0]
        diffuse_attr = pm.listConnections(shader.color, source=1, destination=0)[0]
        if diffuse_attr.type() == 'file':
            return diffuse_attr.fileTextureName.get()
        else:
            for i in pm.listHistory(diffuse_attr):
                if i.type() == 'file':
                    if 'CLR' or 'DIFF' in i.fileTextureName.get():
                        return i.fileTextureName.get()
    except:
        return None
        
                    
def set_attribute(name):
    for mesh in get_all_meshes():
        if get_color_texture(mesh):
            pm.setAttr(pm.PyNode('%s.mtoa_constant_%s' % (mesh, name)), get_color_texture(mesh), type='string')
        

def create_shader(name):
    if not pm.objExists('user_data_string_%s' % name):
        user_shader = pm.shadingNode('aiUserDataString', asShader=1, name='user_data_string_%s' % name)
    else:
        user_shader = pm.PyNode('user_data_string_%s' % name)
    user_shader.stringAttrName.set(name)
    if not pm.objExists('aov_file_%s' % name):
        file_node = pm.shadingNode('file', asTexture=1, name='aov_file_%s' % name)
    else:
        file_node = pm.PyNode('aov_file_%s' % name)
    user_shader.outValue >> file_node.fileTextureName
    if not pm.objExists('aov_utility_%s' % name):
        utility_shader = pm.shadingNode('aiUtility', asShader=1, name='aov_utility_%s' % name)
    else:
        utility_shader = pm.PyNode('aov_utility_%s' % name)
    utility_shader.shadeMode.set(2)
    file_node.outColor >> utility_shader.color
    return utility_shader
    
    
def add_aov(name):
    if pm.PyNode('defaultRenderGlobals').currentRenderer.get() == 'arnold':
        if not name in get_aov_name_lists():
            try:
                aovs.AOVInterface().addAOV(name)
            except:pass
        pm.PyNode('aiAOV_%s.type' % name).set(5)
        pm.PyNode('aiAOV_%s.enabled' % name).set(1)
        
        
def create_aov(name):
    rebuild_arnold_aov()
    print '[OF] info: rebulid successful'
    add_attribute(name)
    print '[OF] info: add attribute successful'
    set_attribute(name)
    print '[OF] info: set attribute successful'
    add_aov(name)
    print '[OF] info: add aov successful'
    shader = create_shader(name)
    print '[OF] info: create shader successful'
    shader.outColor >> pm.PyNode('aiAOV_%s' % name).defaultValue
    print 'finished'
    
    
def main():
    create_aov('diffuse')
    
    
if __name__ == '__main__':
    main()