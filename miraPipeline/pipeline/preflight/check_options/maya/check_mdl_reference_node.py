# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        reference_nodes = self.get_reference_node()
        if not reference_nodes:
            self.pass_check(u"没有reference节点存在")
        else:
            self.error_list = self.get_reference_node()
            self.fail_check(u"模型大组下有reference节点存在")

    @staticmethod
    def get_reference_node():
        references = list()
        selected = mc.ls(sl=1)
        children = mc.listRelatives(selected[0], ad=1)
        for i in children:
            if mc.referenceQuery(i, isNodeReferenced=1):
                references.append(i)
        return references


if __name__ == "__main__":
    pass
