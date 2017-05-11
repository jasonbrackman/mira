# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class check_sceneset_no_char(BaseCheck):

    def run(self):
        self.error_list = self.get_not_env()
        if self.error_list:
            self.fail_check(u"有不是场景和道具的资产存在")
        else:
            self.pass_check(u"资产正确")

    def get_not_env(self):
        not_env = list()
        references = mc.file(r=1, q=1, withoutCopyNumber=1)
        for ref in references:
            obj = pipeFile.PathDetails.parse_path(ref)
            asset_type = obj.asset_type
            if asset_type not in ["environment", "prop"]:
                not_env.append(ref)
        return not_env
