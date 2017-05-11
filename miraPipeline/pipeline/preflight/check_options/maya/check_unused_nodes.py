# -*- coding: utf-8 -*-
from miraLibs.mayaLibs import delete_unused_nodes
from BaseCheck import BaseCheck


class check_unused_nodes(BaseCheck):
    def run(self):
        try:
            delete_unused_nodes.delete_unused_nodes()
            self.pass_check(u"无用节点已被删除")
        except Exception as e:
            self.fail_check(u"有些无用节点不能被删除")
