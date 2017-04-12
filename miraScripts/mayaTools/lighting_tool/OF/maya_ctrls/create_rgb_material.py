__author__ = 'heshuai'


import maya.cmds as mc


def create_rgb_material():
    if not mc.pluginInfo('Mayatomr.mll',loaded = 1,q = 1):
        mc.loadPlugin('Mayatomr.mll',quiet = 1)
    if not mc.objExists('red_mat'):
        red = mc.shadingNode('surfaceShader',asShader = 1,name = 'red_mat')
        redSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'red_SG')
        mc.connectAttr(red + '.outColor' ,redSG + '.surfaceShader',force = 1)
        mc.setAttr(red + '.outColor', 1,0,0,type = 'double3')
        mc.setAttr(red + '.outMatteOpacity', 0,0,0,type = 'double3')
    if not mc.objExists('redx_mat'):
        redx = mc.shadingNode('surfaceShader',asShader = 1,name = 'redx_mat')
        redxSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'redx_SG')
        mc.connectAttr(redx + '.outColor' ,redxSG + '.surfaceShader',force = 1)
        mc.setAttr(redx + '.outColor', 1,0,0,type = 'double3')
        mc.setAttr(redx + '.outMatteOpacity', 1,1,1,type = 'double3')
    if not mc.objExists('green_mat'):
        green = mc.shadingNode('surfaceShader',asShader = 1,name = 'green_mat')
        greenSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'green_SG')
        mc.connectAttr(green + '.outColor' ,greenSG + '.surfaceShader',force = 1)
        mc.setAttr(green + '.outColor', 0,1,0,type = 'double3')
        mc.setAttr(green + '.outMatteOpacity', 0,0,0,type = 'double3')
    if not mc.objExists('greenx_mat'):
        greenx = mc.shadingNode('surfaceShader',asShader = 1,name = 'greenx_mat')
        greenxSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'greenx_SG')
        mc.connectAttr(greenx + '.outColor' ,greenxSG + '.surfaceShader',force = 1)
        mc.setAttr(greenx + '.outColor', 0,1,0,type = 'double3')
        mc.setAttr(greenx + '.outMatteOpacity', 1,1,1,type = 'double3')     
    if not mc.objExists('blue_mat'):
        blue = mc.shadingNode('surfaceShader',asShader = 1,name = 'blue_mat')
        blueSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'blue_SG')
        mc.connectAttr(blue + '.outColor' ,blueSG + '.surfaceShader',force = 1)
        mc.setAttr(blue + '.outColor', 0,0,1,type = 'double3')
        mc.setAttr(blue + '.outMatteOpacity', 0,0,0,type = 'double3')       
    if not mc.objExists('bluex_mat'):
        bluex = mc.shadingNode('surfaceShader',asShader = 1,name = 'bluex_mat')
        bluexSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'bluex_SG')
        mc.connectAttr(bluex + '.outColor' ,bluexSG + '.surfaceShader',force = 1)
        mc.setAttr(bluex + '.outColor', 0,0,1,type = 'double3')
        mc.setAttr(bluex + '.outMatteOpacity', 1,1,1,type = 'double3') 
    if not mc.objExists('black_mat'):
        black = mc.shadingNode('surfaceShader',asShader = 1,name = 'black_mat')
        blackSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'black_SG')
        mc.connectAttr(black + '.outColor' ,blackSG + '.surfaceShader',force = 1)
        mc.setAttr(black + '.outColor', 0,0,0,type = 'double3') 
        mc.setAttr(black + '.outMatteOpacity', 0,0,0,type = 'double3') 
    if not mc.objExists('white_mat'):         
        white = mc.shadingNode('surfaceShader',asShader = 1,name = 'white_mat')
        whiteSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'white_SG')
        mc.connectAttr(white + '.outColor' ,whiteSG + '.surfaceShader',force = 1)
        mc.setAttr(white + '.outColor', 0,0,0,type = 'double3') 
        mc.setAttr(white + '.outMatteOpacity', 1,1,1,type = 'double3') 
    if not mc.objExists('sheen_mat'):
        sheen = mc.shadingNode('surfaceShader',asShader = 1,name = 'sheen_mat')
        sheenSG = mc.sets( noSurfaceShader = 1,renderable = 1,empty = 1,name = 'sheen_SG')
        mc.connectAttr(sheen+'.outColor',sheenSG + '.surfaceShader',force = 1)
        mc.setAttr(sheen + '.outMatteOpacity', 0,0,0,type = 'double3') 
        sampInfo = mc.shadingNode('samplerInfo',asUtility = 1,name = 'sampInfo_mat')
        ramp = mc.shadingNode('ramp',asTexture = 1,name = 'ramp_mat')
        mc.connectAttr(sampInfo+'.facingRatio',ramp+'.vCoord',force = 1)
        mc.connectAttr(ramp+'.outColor',sheen+'.outColor',force = 1)
        mc.removeMultiInstance(ramp+'.colorEntryList[1]',b = 1)
        mc.setAttr(ramp+'.colorEntryList[2].color',0,0,0,type = 'double3')
        mc.setAttr(ramp+'.colorEntryList[0].color',1,1,1,type = 'double3')
        mc.setAttr(ramp+'.colorEntryList[2].position',0.75)

    ########create mentalray shadow shader
    '''
    if not mc.objExists('matteShadow_mat'):
        alpha = mc.shadingNode('mib_color_alpha',asUtility = 1,name = 'alpha_mat')
        mc.setAttr(alpha+'.factor',0)
        matte = mc.shadingNode('mip_matteshadow',asShader = 1,name = 'matteShadow_mat')
        mc.setAttr(matte+'.ambient',0,0,0,type = 'double3')
        mc.setAttr(matte+'.ao_on',0)
        shadowSG = mc.sets(renderable = 1,noSurfaceShader = 1,empty = 1,name = 'shadow_SG')
        mc.connectAttr(matte+'.message',shadowSG+'.miMaterialShader')
        mc.connectAttr(alpha+'.outValue',matte+'.background',f = 1)
        mc.connectAttr(alpha+'.outValueA',matte+'.backgroundA',f = 1)
    '''

    ########create arnold shadow shader
    if mc.objExists('shaodw_SG'):
        mc.delete('shaodw_SG')
    if mc.objExists('shadow_catcher'):
        mc.delete('shadow_catcher')
    if mc.objExists('shadow_SG'):
        mc.delete('shadow_SG')
    shadow_shader = mc.shadingNode('aiUtility', asShader=1, name='shaodw_SG')
    shadow_catcher = mc.shadingNode('aiShadowCatcher', asShader=1, name='shadow_catcher')
    shadow_sg = mc.sets(renderable=1, noSurfaceShader=1, empty=1, name='shadow_SG')
    mc.setAttr('shaodw_SG.shadeMode', 2)
    mc.setAttr('shadow_catcher.enableTransparency', 1)
    mc.connectAttr('shadow_catcher.outColor', 'shaodw_SG.color')
    mc.connectAttr('shaodw_SG.outColor', 'shadow_SG.surfaceShader')