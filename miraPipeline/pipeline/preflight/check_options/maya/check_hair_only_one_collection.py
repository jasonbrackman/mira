# -*- coding: utf-8 -*-
import xgenm as xgen
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile


class Check(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if not self.error_list:
            self.pass_check(u"collection只有一个且命名正确")
            return
        if len(self.error_list) > 1:
            self.fail_check(u"不止一个collection。")
        elif len(self.error_list) == 1:
            self.pass_check(u"collection命名不正确。")

    def get_error_list(self):
        collections = xgen.palettes()
        if len(collections) > 1:
            return collections
        elif len(collections) == 1:
            collection_name = collections[0]
            context = pipeFile.PathDetails.parse_path()
            asset_name = context.asset_name
            if collection_name != "%s_collection" % asset_name:
                return collections
