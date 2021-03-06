# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_all_cameras, get_scene_name


def get_valid_camera(file_path=None):
    if not file_path:
        file_path = get_scene_name.get_scene_name()
    context = pipeFile.PathDetails.parse_path(file_path)
    seq_name = context.sequence
    shot_name = context.shot
    valid_camera = "cam_%s_%s" % (seq_name, shot_name)
    cameras = get_all_cameras.get_all_camera_transforms()
    valid_cameras = [camera for camera in cameras if camera.endswith(valid_camera)]
    if len(valid_cameras) != 1:
        return
    else:
        return valid_cameras[0]
