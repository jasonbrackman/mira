# -*- coding: utf-8 -*-
import logging
import playblaster
from miraLibs.mayaLibs import set_image_size
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraLibs.mayaLibs import get_frame_range
from miraLibs.pipeLibs.pipeMaya import get_valid_camera
from miraLibs.pyLibs import create_parent_dir
from miraLibs.pipeLibs.copy import Copy


def playblast_shot():
    logger = logging.getLogger(__name__)
    valid_camera = get_valid_camera.get_valid_camera()
    if not valid_camera:
        raise Exception("No valid camera found.")
    frame_range = get_frame_range.get_frame_range()
    obj = pipeFile.PathDetails.parse_path()
    current_project = obj.project
    resolution = pipeMira.get_resolution(current_project)
    percent = pipeMira.get_playblast_percent(current_project)
    set_image_size.set_image_size(*resolution)
    local_video_path = obj.local_video_path
    video_path = obj.video_path
    create_parent_dir.create_parent_dir(local_video_path)
    playblaster.playblaster(local_video_path, valid_camera, frame_range[0], frame_range[1],
                            resolution, percent, open_it=True)
    logger.info("Playblast to %s" % local_video_path)
    # backup video path
    Copy.copy(local_video_path, video_path)
    logger.info("Copy %s >> %s" % (local_video_path, video_path))
