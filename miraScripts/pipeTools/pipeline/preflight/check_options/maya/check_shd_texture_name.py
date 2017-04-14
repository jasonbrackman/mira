# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class check_shd_texture_name(BaseCheck):

    def __init__(self):
        BaseCheck.__init__(self)
        obj = pipeFile.PathDetails.parse_path()
        asset_name = obj.asset_name
        shd_version = obj.shd_version
        self.prefix = "%s_%s_" % (asset_name, shd_version)
        self.suffix_list = ["_dif", "_spe", "_bmp", "_nml", "_dmp", "_shallow", "_env",
                            "_mid", "_dep", "_rfl", "_rfr", "_blendmask", "_op", "_rgh", "_ior"]
        self.file_nodes = mc.ls(type="file")
        self.all_textures = None
        if self.file_nodes:
            all_textures = [mc.getAttr("%s.computedFileTextureNamePattern" % f) for f in self.file_nodes]
            self.all_textures = list(set(all_textures))

    def run(self):
        self.error_list = self.get_invalid_prefix(self.all_textures) + self.get_invalid_suffix(self.all_textures)
        if self.error_list:
            tip_string = u"贴图必须以%s开始，以%s结尾" % (self.prefix, self.suffix_list)
            self.fail_check(u"贴图命名不正确\n%s" % tip_string)
        else:
            self.pass_check(u"贴图命名正确")

    def get_invalid_suffix(self, textures):
        if not textures:
            return
        invalid_suffix = list()
        for texture in textures:
            texture_base_name = os.path.basename(texture)
            prefix, ext = os.path.splitext(texture_base_name)
            if not any([prefix.endswith(suffix) for suffix in self.suffix_list]):
                invalid_suffix.append(texture)
        return invalid_suffix

    def get_invalid_prefix(self, textures):
        if not textures:
            return
        invalid_prefix = list()
        for texture in textures:
            texture_base_name = os.path.basename(texture)
            if texture_base_name.startswith(self.prefix):
                continue
            invalid_prefix.append(texture)
        return invalid_prefix
