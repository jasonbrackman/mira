# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
import playblaster
from miraBake import remove_turntable
from miraLibs.mayaLibs import set_image_size
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pipeLibs.pipeMaya import get_model_name
from miraLibs.pyLibs import create_parent_dir
from miraPipeline.maya.asset_turntable import create_turntable
reload(create_turntable)


def playblast_turntable(submit=True):
    logger = logging.getLogger(__name__)
    # get path
    obj = pipeFile.PathDetails.parse_path()
    local_video_path = obj.local_video_path
    work_video_path = obj.work_video_path
    current_project = obj.project
    # playblast
    model_name = get_model_name.get_model_name()
    resolution = pipeMira.get_resolution(current_project)
    percent = pipeMira.get_playblast_percent(current_project)
    set_image_size.set_image_size(*resolution)
    mc.select(model_name, r=1)
    cam = create_turntable.create_turntable()
    create_parent_dir.create_parent_dir(local_video_path)
    playblaster.playblaster(local_video_path, cam, 1, 240, resolution, percent, False, None, True)
    remove_turntable.remove_turntable()
    logger.info("playblast done.")
    mc.lookThru("persp")
    if submit:
        Copy.copy(local_video_path, work_video_path)
        logger.info("Copy %s >> %s" % (local_video_path, work_video_path))
        return work_video_path
    else:
        return local_video_path
