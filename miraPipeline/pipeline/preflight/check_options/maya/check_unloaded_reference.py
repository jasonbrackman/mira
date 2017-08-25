# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = self.get_unload_reference()
        if self.error_list:
            self.fail_check(u"有reference没有加载")
        else:
            self.pass_check(u"所有reference已加载")

    @staticmethod
    def get_unload_reference():
        all_ref = pm.listReferences()
        unloaded_refs = [ref for ref in all_ref if not ref.isLoaded()]
        return unloaded_refs

    def auto_solve(self):
        self.error_list = list()
        unload_reference = self.get_unload_reference()
        for ref in unload_reference:
            try:
                ref.remove()
            except:
                self.error_list.append(ref)
        if self.error_list:
            self.fail_check(u"有些reference不能被移除")
        else:
            self.pass_check(u"没有加载的reference已经被移除")
