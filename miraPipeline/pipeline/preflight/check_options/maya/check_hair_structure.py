# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile


class Check(BaseCheck):

    def run(self):
        context = pipeFile.PathDetails.parse_path()
        asset_type_short_name = context.asset_type_short_name
        asset_name = context.asset_name
        sculp_group = "%s_%s_SCULP" % (asset_type_short_name, asset_name)
        collection_name = "%s_collection" % asset_name
        top_nodes = mc.ls(assemblies=1)
        if sculp_group in top_nodes and collection_name in top_nodes:
            self.pass_check(u"大纲结构正确")
        else:
            self.fail_check(u"大纲结构不正确")
