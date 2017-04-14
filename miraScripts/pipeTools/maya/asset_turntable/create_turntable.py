# -*- coding: utf-8 -*-
import logging
import pymel.core as pm
import maya.cmds as mc


def create_turntable():
    # # save current file
    # mc.file(save=1, f=1)
    # sel the group for turntable
    sel = mc.ls(sl=1)
    group_name = "tt_rotation"
    cam_name = "tt_camera"
    if sel:
        if pm.ls(group_name):
            logging.warning("tt_rotation group exist.")
            return
        else:
            child = mc.listRelatives(sel, children=True, ad=True)
            bb = mc.exactWorldBoundingBox(child)
            center = mc.objectCenter(sel)
            distance = max([abs(each) for each in bb])
            distance *= 2.42
            # group the sel as tt_rotation
            mc.group(n="tt_rotation")
            # mc.parent(sel, "tt_rotation")
            # create camera
            camera = mc.camera(n=cam_name, coi=distance)[0]
            mc.rename(camera, cam_name)
            mc.setAttr("%s.visibility" % cam_name, 0)
            mc.move(center[0], center[1], abs(center[2])+distance, cam_name)
            # key the tt_rotation group
            mc.setKeyframe("tt_rotation", value=0, t=0, itt="linear", ott="linear", at="rotateY")
            mc.setKeyframe('tt_rotation', v=360, t=300, itt='linear', ott='linear', at='rotateY')
            # set animation range
            mc.playbackOptions(minTime=0, animationStartTime=0)
            mc.playbackOptions(maxTime=300, animationEndTime=300)
            # look though the camera
            mc.lookThru(cam_name, nearClip=0.001, farClip=1000)
            return True
    else:
        logging.error('No object selected, please select an object')
        return False


if __name__ == "__main__":
    create_turntable()
