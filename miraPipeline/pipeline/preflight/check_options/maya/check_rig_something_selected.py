# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs.pipeMaya import get_model_name
from BaseCheck import BaseCheck


class check_rig_something_selected(BaseCheck):
    def __init__(self):
        super(check_rig_something_selected, self).__init__()
        self.rig_root_name = get_model_name.get_model_name(typ="rig")

    def run(self):
        selected_objects = mc.ls(sl=1)
        if not selected_objects:
            self.fail_check(u"没有选中ROOT大组")
        else:
            if len(selected_objects) > 1:
                self.fail_check(u"不止一个物体被选中")
                return
            if selected_objects[0] == self.rig_root_name:
                self.pass_check("Select %s" % self.rig_root_name)
            else:
                self.fail_check(u"没有选中%s" % self.rig_root_name)

    def auto_solve(self):
        if mc.objExists(self.rig_root_name):
            mc.select(self.rig_root_name, r=1)
            self.pass_check("Select %s" % self.rig_root_name)
        else:
            self.fail_check(u"{0}不存在>".format(self.rig_root_name))
