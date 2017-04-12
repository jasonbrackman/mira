# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
import playblaster
from miraLibs.mayaLibs import set_image_size
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraLibs.pipeLibs.pipeMaya import get_model_name
from miraScripts.pipeTools.asset_turntable import create_turntable, remove_turntable
from miraLibs.pyLibs import create_parent_dir
from miraLibs.pipeLibs.copy import Copy


def playblast_turntable():
    logger = logging.getLogger(__name__)
    # get path
    obj = pipeFile.PathDetails.parse_path()
    local_video_path = obj.local_video_path
    video_path = obj.video_path
    current_project = obj.project
    # playblast
    model_name = get_model_name.get_model_name()
    resolution = pipeMira.get_resolution(current_project)
    percent = pipeMira.get_playblast_percent(current_project)
    set_image_size.set_image_size(*resolution)
    mc.select(model_name, r=1)
    create_turntable.create_turntable()
    create_parent_dir.create_parent_dir(local_video_path)
    playblaster.playblaster(local_video_path, "tt_camera", 1, 300, resolution, percent, False, None, True)
    remove_turntable.remove_turntable()
    logger.info("playblast done.")
    Copy.copy(local_video_path, video_path)
    logger.info("Copy %s >> %s" % (local_video_path, video_path))
    mc.lookThru("persp")
