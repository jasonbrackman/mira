# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_needed_camera():
    exclude_camera = ['frontShape', 'perspShape', 'sideShape', 'topShape']
    all_cameras = mc.ls(cameras=1)
    cameras = list(set(all_cameras)-set(exclude_camera))
    cameras = [mc.listRelatives(camera, parent=1)[0] for camera in cameras]
    return cameras
