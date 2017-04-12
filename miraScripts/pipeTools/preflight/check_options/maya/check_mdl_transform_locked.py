# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck


class check_mdl_transform_locked(BaseCheck):

    def run(self):
        selected = pm.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_unlock_attributes()
        if self.error_list:
            self.fail_check(u"模型的旋转缩放位移属性没锁定")
        else:
            self.pass_check(u"模型的旋转缩放位移属性全部锁定")

    def get_child_transform(self, parent_object):
        children_transform = pm.listRelatives(parent_object, allDescendents=1, type="transform")
        return children_transform

    def get_unlock_attributes(self):
        unlock_attributes = list()
        # get model name
        model_name = pm.ls(sl=1)[0]
        # get child transform
        children_transform = self.get_child_transform(model_name)
        base_attributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
        for transform in children_transform:
            for attr in base_attributes:
                if not transform.getAttr(attr, lock=True):
                    unlock_attributes.append("%s.%s" % (transform.name(), attr))
        return unlock_attributes

    def auto_solve(self):
        self.error_list = list()
        unlock_attributes = self.get_unlock_attributes()
        for attr in unlock_attributes:
            try:
                pm.setAttr(attr, lock=1)
            except:
                self.error_list.append(attr)
        if self.error_list:
            self.fail_check(u"有些模型属性不能被锁定")
        else:
            self.pass_check(u"所有模型旋转位移缩放属性被锁定")


if __name__ == "__main__":
    pass
