# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_backup_visibility_unlocked(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        backup_group = self.get_backup_group()
        if len(backup_group) != 1:
            self.fail_check(u"_BACKUP组的个数不为1")
            return
        visibility_is_lock = mc.getAttr("%s.visibility" % backup_group[0], l=1)
        if visibility_is_lock:
            self.error_list = backup_group
            self.fail_check(u"_BACKUP组的显示属性未被锁定")
        else:
            self.pass_check(u"_BACKUP组的显示属性已被锁定")

    @staticmethod
    def get_backup_group():
        selected = mc.ls(sl=1)[0]
        children = mc.listRelatives(selected, ad=1, type="transform")
        backup_trans = [trans for trans in children if trans.endswith("_BACKUP")]
        return backup_trans

    def auto_solve(self):
        self.error_list = list()
        backup_group = self.get_backup_group()
        try:
            mc.setAttr("%s.visibility" % backup_group[0], l=0)
        except:
            self.error_list.append(backup_group[0])
        if self.error_list:
            self.fail_check(u"_BACKUP组的显示属性不能被解锁")
        else:
            self.pass_check(u"_BACKUP组的显示属性被解锁")

