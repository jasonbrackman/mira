# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs import Project
from miraLibs.mayaLibs import create_reference, create_group


def import_camera(project, sequence, step):
    db = db_api.DbApi(project).db_obj
    shots = db.get_all_shots(sequence)
    if not shots:
        print "No shot exist in this sequence"
        return
    shot_names = [shot.get("code") for shot in shots]
    for shot_name in shot_names:
        cache_template = Project(project).template("maya_shot_cache")
        cache_dir = cache_template.format(project=project, sequence=sequence,
                                          shot=shot_name.split("_")[-1], step=step, task=step)
        camera_cache_path = "%s/camera.abc" % cache_dir
        if not os.path.isfile(camera_cache_path):
            print "%s is not exist." % camera_cache_path
            continue
        create_reference.create_reference(camera_cache_path)
    group_camera()


def group_camera():
    create_group.create_group("Camera")
    exclude_grp = ['frontShape', 'perspShape', 'sideShape', 'topShape']
    for camera in mc.ls(cameras=1):
        if camera not in exclude_grp:
            transform = mc.listRelatives(camera, p=1)[0]
            mc.parent(transform, "Camera")
