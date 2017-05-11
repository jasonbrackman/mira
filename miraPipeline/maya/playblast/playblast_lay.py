# -*- coding: utf-8 -*-
import logging
import os
import maya.cmds as mc
import playblaster
reload(playblaster)
from miraLibs.mayaLibs import set_image_size
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraLibs.pyLibs import create_parent_dir
from miraLibs.pipeLibs.copy import Copy
from miraLibs.mayaLibs import get_frame_range


class PlayblastLay(object):
    def __init__(self):
        self.logger = logging.getLogger("Playblast Lay")
        self.obj = pipeFile.PathDetails.parse_path()
        self.current_project = self.obj.project
        self.resolution = pipeMira.get_resolution(self.current_project)
        set_image_size.set_image_size(*self.resolution)
        self.percent = pipeMira.get_playblast_percent(self.current_project)
        self.local_dir = pipeMira.get_local_root_dir(self.current_project)

    def playblast_lay(self):
        # get sequencer frame range
        # get paths and project settings
        local_video_path = self.obj.local_video_path
        video_path = self.obj.video_path
        start_frame, end_frame = get_frame_range.get_frame_range()
        # playblast to local
        create_parent_dir.create_parent_dir(local_video_path)
        playblaster.playblaster(local_video_path, None, start_frame, end_frame, self.resolution, self.percent,
                                open_it=True, use_sequence_time=False)
        self.logger.info("Playblast to %s" % local_video_path)
        # copy to server
        Copy.copy(local_video_path, video_path)
        self.logger.info("Copy %s >> %s" % (local_video_path, video_path))

    def playblast_lay_shots(self):
        shot_nodes = mc.ls(type="shot")
        if not shot_nodes:
            raise Exception("No shot node found")
        for shot_node in shot_nodes:
            self.playblast_lay_single_shot(shot_node)

    def playblast_lay_single_shot(self, shot_node):
        camera = mc.listConnections("%s.currentCamera" % shot_node, s=1, d=0)
        if not camera:
            self.logger.error("No camera connect to %s" % shot_node)
            return
        start_frame = mc.getAttr("%s.startFrame" % shot_node)
        end_frame = mc.getAttr("%s.endFrame" % shot_node)
        shot_type, seq, shot = shot_node.split("_")
        video_path = pipeFile.get_shot_step_video_file(seq, shot, "lay", self.current_project)
        prefix, suffix = os.path.splitdrive(video_path)
        local_video_path = os.path.join(self.local_dir, suffix).replace("\\", "/")
        playblaster.playblaster(local_video_path, camera[0], start_frame, end_frame, self.resolution, self.percent,
                                open_it=False)
        self.logger.info("Playblast to %s" % local_video_path)
        Copy.copy(local_video_path, video_path)
        self.logger.info("Copy %s >> %s" % (local_video_path, video_path))
