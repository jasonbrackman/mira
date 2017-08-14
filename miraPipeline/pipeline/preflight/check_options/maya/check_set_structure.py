# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile


class check_set_structure(BaseCheck):

    def run(self):
        context = pipeFile.PathDetails.parse_path()
        env_grp = "%s_env" % context.sequence
        if not mc.objExists(env_grp):
            self.fail_check(u"%s 不存在。" % env_grp)
            return
        top_groups = mc.ls(assemblies=1)
        if env_grp in top_groups:
            self.pass_check(u"大纲结构正确")
        else:
            self.fail_check(u"%s不在最外层" % env_grp)
