# -*- coding: utf-8 -*-
import os
from BaseCheck import BaseCheck
from miraLibs.mayaLibs import Yeti, get_all_hair_textures


class check_hair_texture_exist(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有贴图不存在")
        else:
            self.pass_check(u"所有的贴图都存在")

    @staticmethod
    def get_error_list():
        error_files = list()
        yt = Yeti.Yeti()
        yeti_textures = yt.get_all_texture_path()
        hair_textures = get_all_hair_textures.get_all_hair_textures()
        all_textures = yeti_textures + hair_textures
        if not all_textures:
            return
        for tex in all_textures:
            if not os.path.isfile(tex):
                error_files.append(tex)
        return error_files
