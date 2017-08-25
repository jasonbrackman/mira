# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        name_spaces = self.get_name_space()
        if name_spaces:
            self.error_list = name_spaces
            self.fail_check(u"有名称空间存在")
        else:
            self.pass_check(u"没有名称空间存在")

    def get_name_space(self):
        selected = mc.ls(sl=1)
        children = mc.listRelatives(selected[0], allDescendents=1)
        namespaces = [":".join(i.split(":")[:-1]) for i in children if ":" in i]
        namespaces = list(set(namespaces))
        return namespaces

    def auto_solve(self):
        namespaces = self.get_name_space()
        if not namespaces:
            self.pass_check(u"没有名称空间存在")
        else:
            mc.namespace(set=":")
            for name in namespaces:
                if name not in ('UI', 'shared'):
                    self.remove_namespace(name)
            self.pass_check(u"名称空间已被删除")

    def remove_namespace(self, namespace_name):
        children = mc.namespaceInfo(namespace_name, listOnlyNamespaces=1)
        if children:
            for child in children:
                self.remove_namespace(child)
        mc.namespace(moveNamespace=(namespace_name, ":"), f=1)
        mc.namespace(removeNamespace=namespace_name)


if __name__ == "__main__":
    pass
