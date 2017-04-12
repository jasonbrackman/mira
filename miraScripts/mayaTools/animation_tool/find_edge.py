# -*- coding: utf-8 -*-
import maya.mel as mm
import maya.cmds as mc


def toggle_camera():
    current_camera = mc.modelEditor(mc.getPanel(withFocus=1),q=1,camera=1)
    camera_list = mc.ls(type='camera')
    for _cam in camera_list :
        cam_transform = mc.listRelatives(_cam,p=1,f=1)
        if cam_transform:
            if mc.getAttr(cam_transform[0]+'.renderable'):
                try:
                    mc.setAttr(cam_transform[0]+'.renderable',0)
                except:
                    pass
                mc.setAttr(current_camera+'.renderable',1)


def find_edge():
    if not mc.ls(sl=1):
        mc.confirmDialog(message="select a mesh,first!")
    toggle_camera()
    sel = mc.ls(sl=1, l=1)[0]
    new_curve_group_name = sel.split('|')[-1] + '_' + str(int(mc.currentTime(q=1))) + '_fps_curveGroup'
    mm.eval('assignPfxToon "" 0;')
    pfx_toon_mesh = mc.ls(sl=1)[0]
    pfx_toon_trans = mc.listRelatives(pfx_toon_mesh, p=1)
    mm.eval('doPaintEffectsToCurve( 0)')
    new_curve_group = pfx_toon_mesh+'Curves'
    final_name = mc.duplicate(new_curve_group, name=new_curve_group_name)
    mc.delete(pfx_toon_trans)
    mc.delete(new_curve_group)
    mc.select(final_name)


if __name__ == "__main__":
    find_edge()