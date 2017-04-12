# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class check_rig_structure(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        sel = selected[0]
        # exclude = ['persp', 'top', 'front', 'side', sel, "_BLENDS"]
        # top_groups = mc.ls(assemblies=1)
        # wrong_list = list()
        # for group in top_groups:
        #     if group not in exclude:
        #         wrong_list.append(group)
        # if wrong_list:
        #     self.warning_check("%s is not organized:\n" % "\n".join(wrong_list))
        obj = pipeFile.PathDetails.parse_path()
        asset_type = obj.asset_type
        children = mc.listRelatives(sel, children=1)
        model_name = sel.replace("_ROOT", "_MODEL")
        if asset_type == "prop":
            rig_name = sel.replace("_ROOT", "_RIG")
            normal_list = [model_name, rig_name]
        elif asset_type == "character":
            normal_list = ["Others", "Geometry", "Grp_Master_Ctl"]
        self.error_list = list(set(children)-set(normal_list))
        if self.error_list:
            self.fail_check(u"大纲层级结构不对")
        else:
            self.pass_check("Group Structure is right.")
