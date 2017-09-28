# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def run(self):
        created_camera = self.get_created_cameras()
        if not created_camera:
            self.fail_check(u"没有摄像机")
            return
        valid_camera = self.get_valid_camera()
        if not mc.objExists(valid_camera):
            self.fail_check(u"摄像机%s不存在" % valid_camera)
        else:
            camera_list = mc.ls(valid_camera)
            if len(camera_list) == 1:
                self.pass_check(u"摄像机正确")
            else:
                self.fail_check(u"有同名摄像机")

    @staticmethod
    def get_created_cameras():
        cameras = mc.ls(cameras=1)
        cameras = [mc.listRelatives(cam, parent=1)[0] for cam in cameras]
        exclude = ["front", "persp", "side", "top"]
        created_cameras = list(set(cameras)-set(exclude))
        return created_cameras

    @staticmethod
    def get_valid_camera():
        context = pipeFile.PathDetails.parse_path()
        seq = context.sequence
        shot = context.shot
        valid_camera = "cam_%s_%s" % (seq, shot)
        return valid_camera
