# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_save_file(BaseCheck):

    def run(self):
        file_unsaved = self.check_file_save()
        if file_unsaved:
            self.fail_check(u"文件已被更改，建议保存")
        else:
            self.pass_check(u"文件无更改")

    @staticmethod
    def check_file_save():
        return mc.file(query=True, anyModified=True) or (not mc.file(query=True, exists=True))

    def auto_solve(self):
        try:
            mc.file(save=1, f=1)
            self.pass_check(u"文件已保存")
        except:
            self.fail_check(u"文件不能被保存")


if __name__ == "__main__":
    pass
