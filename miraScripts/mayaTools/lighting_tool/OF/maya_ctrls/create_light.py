__author__ = 'heshuai'


import maya.cmds as mc
import maya.mel as  mel


def create_directional_light():
    mc.directionalLight()


def create_point_light():
    mc.pointLight()


def create_spot_light():
    mc.spotLight()


def create_area_light():
    mel.eval('CreateAreaLight;')


def create_sky_dome_light():
    all_sky_light = mc.ls(type='aiSkyDomeLight')
    if len(all_sky_light) >= 1:
        ret = mc.confirmDialog(message='aiSkyDomeLight exists,Do you want to create more?', icon='information', button=['Yes', 'No'], title='warm tip', messageAlign='center')
        if ret == 'Yes':
            sky_dome_light()
    else:
        sky_dome_light()
        
            
def sky_dome_light():
    file_node = mc.shadingNode('file', asTexture=1, name='IBL_light_file')
    env_light = mc.shadingNode('aiSkyDomeLight', asLight=1, name='ai_sky_dome_light_shape')
    light_shape = mc.ls(env_light, ap=1, dag=1, lf=1)[0]
    mc.connectAttr('%s.outColor' % file_node, '%s.color' % light_shape, force=1)
    mc.rename(env_light, 'ai_sky_dome_light')