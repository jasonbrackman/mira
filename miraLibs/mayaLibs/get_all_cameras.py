# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_all_cameras():
    exclude = ["frontShape", "perspShape", "sideShape", "topShape"]
    cameras = mc.ls(cameras=1)
    cameras = list(set(cameras)-set(exclude))
    return cameras


def get_all_camera_transforms():
    cameras = get_all_cameras()
    camera_transforms = [mc.listRelatives(camera, p=1)[0] for camera in cameras]
    return camera_transforms
