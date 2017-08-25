# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def __init__(self):
        super(Check, self).__init__()
        obj = pipeFile.PathDetails.parse_path()
        asset_name = obj.asset_name
        asset_type_short_name = obj.asset_type_short_name
        self.render_grp = "%s_%s_hair_render_grp" % (asset_type_short_name, asset_name)

    def run(self):
        if self.render_exist():
            self.pass_check(u"%s存在" % self.render_grp)
        else:
            self.fail_check(u"%s不存在" % self.render_grp)

    def render_exist(self):
        if mc.objExists(self.render_grp):
            return True
        else:
            return False
