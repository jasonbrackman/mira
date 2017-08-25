# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        extra_camera = mc.listRelatives(selected[0], allDescendents=1, type="camera")
        if not extra_camera:
            self.pass_check(u"没有多余的相机")
        else:
            self.error_list = extra_camera
            self.fail_check(u"有多余的相机存在")

    def auto_solve(self):
        self.error_list = list()
        selected = mc.ls(sl=1)
        extra_camera = mc.listRelatives(selected[0], allDescendents=1, type="camera")
        if extra_camera:
            for cam in extra_camera:
                camera = mc.listRelatives(cam, p=1)
                is_locked = mc.lockNode(camera, q=1, l=1)[0]
                if is_locked:
                    mc.lockNode(camera, l=0)
                try:
                    mc.delete(camera)
                except:
                    self.error_list.append(camera)
            if self.error_list:
                self.fail_check(u"有些相机不能被删除")
            else:
                self.pass_check(u"多余的相机已经被全部删除")
        else:
            self.pass_check(u"没有多余的相机")
