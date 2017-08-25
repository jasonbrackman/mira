# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        obj = pipeFile.PathDetails.parse_path()
        asset_type_short_name = obj.asset_type_short_name
        asset_name = obj.asset_name
        yeti_node = "%s_%s_yetiNode" % (asset_type_short_name, asset_name)
        if mc.objExists(yeti_node):
            self.pass_check(u"yeti节点%s存在" % yeti_node)
        else:
            self.fail_check(u"yeti节点%s不存在" % yeti_node)
