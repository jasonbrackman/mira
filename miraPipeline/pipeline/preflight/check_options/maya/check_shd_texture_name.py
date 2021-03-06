# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def __init__(self):
        BaseCheck.__init__(self)
        context = pipeFile.PathDetails.parse_path()
        asset_name = context.asset_name
        shd_version = context.task
        self.prefix = "%s_%s_" % (asset_name, shd_version)
        self.suffix_list = ["_dif", "_spe", "_bmp", "_nml", "_dmp", "_shallow", "_env",
                            "_mid", "_dep", "_rfl", "_rfr", "_blendmask", "_op", "_rgh", "_ior"]
        self.file_nodes = mc.ls(type="file")

    def run(self):
        self.error_list = self.get_invalid_suffix(self.file_nodes)
        if self.error_list:
            tip_string = u"贴图必须以%s结尾" % (self.suffix_list)
            self.fail_check(u"贴图命名不正确\n%s" % tip_string)
        else:
            self.pass_check(u"贴图命名正确")

    def get_invalid_suffix(self, file_nodes):
        invalid_suffix = list()
        for file_node in file_nodes:
            texture = mc.getAttr("%s.computedFileTextureNamePattern" % file_node)
            texture_base_name = os.path.basename(texture)
            prefix, ext = os.path.splitext(texture_base_name)
            if not any([prefix.endswith(suffix) for suffix in self.suffix_list]):
                invalid_suffix.append(file_node)
        return invalid_suffix
