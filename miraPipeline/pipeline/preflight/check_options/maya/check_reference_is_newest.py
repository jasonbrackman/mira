# -*- coding: utf-8 -*-
import os
import pymel.core as pm
from miraLibs.pyLibs import get_latest_version
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.error_list = [ref.name() for ref in self.error_list]
            self.fail_check(u"有些reference文件不是最新版本的文件")
        else:
            self.pass_check(u"所有reference文件是最新的版本")

    def get_error_list(self):
        references = pm.listReferences()
        if not references:
            self.pass_check("No reference file found.")
            return
        not_newest_reference = list()
        for ref in pm.listReferences():
            ref_node = ref.refNode
            path = ref_node.referenceFile().path
            latest_version_list = get_latest_version.get_latest_version(path)
            if not latest_version_list:
                continue
            latest_version = latest_version_list[0]
            if os.path.normpath(path) != os.path.normpath(latest_version):
                not_newest_reference.append(ref_node)
        return not_newest_reference

    def auto_solve(self):
        reference_nodes = self.get_error_list()
        if not reference_nodes:
            self.pass_check(u"没有不是最新的reference文件")
            return
        for ref_node in reference_nodes:
            path = ref_node.referenceFile().path
            latest_version = get_latest_version.get_latest_version(path)
            if latest_version:
                rn = pm.system.FileReference(ref_node)
                rn.replaceWith(latest_version[0])
            self.pass_check(u"所有的reference文件已被更新")
