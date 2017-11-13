# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        poly_transfer_nodes = mc.ls(type="polyTransfer")
        if not poly_transfer_nodes:
            self.pass_check("No polyTransfer nodes exist.")
            return
        references = mc.ls(type="reference")
        if references:
            self.fail_check(u"因为有UV传递信息，建议导入reference之后，执行后面的操作")
        else:
            self.pass_check(u"没有reference。")
