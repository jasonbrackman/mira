# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class check_anim_valid_camera(BaseCheck):
    def run(self):
        created_camera = self.get_created_cameras()
        if not created_camera:
            self.fail_check(u"没有摄像机")
            return
        valid_camera = self.get_valid_camera()
        if not mc.objExists(valid_camera):
            self.fail_check(u"相机%s不存在" % valid_camera)
            return
        self.error_list = list(set(created_camera)-set([valid_camera]))
        if self.error_list:
            self.fail_check(u"有多余的摄像机")
        else:
            frame_range_is_exist = mc.ls("%s.frame_range" % valid_camera)
            if frame_range_is_exist:
                self.pass_check(u"相机正确")
            else:
                self.pass_check(u"相机%s上没有添加frame_range属性" % valid_camera)

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
