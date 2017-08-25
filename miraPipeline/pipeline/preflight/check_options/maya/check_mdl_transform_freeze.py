# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = pm.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        # get all xforms
        top_node = pm.ls(sl=1)[0]
        hierarchy_xfroms = top_node.getChildren(allDescendents=True, type="transform")
        hierarchy_xfroms.append(top_node)
        # freeze directly
        locked_attr_list = []
        for xform in hierarchy_xfroms:
            pm.move(0, 0, 0, [xform+'.scalePivot', xform+'.rotatePivot'])
            # check locked attrs
            base_attributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
            for attr in base_attributes:
                if xform.getAttr(attr, lock=True):
                    locked_attr_name = "%s.%s" % (xform, attr)
                    locked_attr_node = pm.PyNode(locked_attr_name)
                    locked_attr_node.unlock()
                    locked_attr_list.append(locked_attr_node)
            # freeze them
            try:
                pm.makeIdentity(xform, apply=True, translate=True, rotate=True, scale=True, n=0, pn=1)
            except RuntimeError, e:
                self.error_list.append(xform.longName())
        # lock again
        for locked_attr_node in locked_attr_list:
            locked_attr_node.lock()
        # feedback
        if self.error_list:
            self.fail_check(u"模型大组下有些模型不能freeze")
        else:
            self.pass_check(u"模型大组下的所有模型被freeze")


if __name__ == "__main__":
    pass
