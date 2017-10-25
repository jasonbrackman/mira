# -*- coding: utf-8 -*-
import os
from BaseCheck import BaseCheck
import nuke
from miraLibs.nukeLibs import save_file


class Check(BaseCheck):

    def run(self):
        file_unsaved = self.check_file_save()
        if file_unsaved:
            self.fail_check(u"文件已被更改，建议保存")
        else:
            self.pass_check(u"文件无更改")

    @staticmethod
    def check_file_save():
        return nuke.root().modified()

    def auto_solve(self):
        try:
            save_file.save_file()
            self.pass_check(u"文件已保存")
        except:
            self.fail_check(u"文件不能被保存")