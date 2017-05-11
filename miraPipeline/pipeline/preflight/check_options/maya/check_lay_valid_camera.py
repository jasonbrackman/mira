# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class check_lay_valid_camera(BaseCheck):
    def run(self):
        created_camera = self.get_created_cameras()
        if not created_camera:
            self.fail_check(u"没有摄像机")
            return
        valid_camera = self.get_valid_camera()
        if not mc.objExists(valid_camera):
            self.fail_check(u"摄像机%s不存在" % valid_camera)
            return
        self.error_list = list(set(created_camera)-set([valid_camera]))
        if self.error_list:
            self.fail_check(u"有多余的摄像机")
        else:
            self.pass_check(u"摄像机正确")

    @staticmethod
    def get_created_cameras():
        cameras = mc.ls(cameras=1)
        cameras = [mc.listRelatives(cam, parent=1)[0] for cam in cameras]
        exclude = ["front", "persp", "side", "top"]
        created_cameras = list(set(cameras)-set(exclude))
        return created_cameras

    @staticmethod
    def get_valid_camera():
        obj = pipeFile.PathDetails.parse_path()
        seq = obj.seq
        shot = obj.shot
        valid_camera = "cam_%s_%s" % (seq, shot)
        return valid_camera
