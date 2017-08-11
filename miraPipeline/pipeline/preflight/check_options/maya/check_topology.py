# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import get_model_name
from miraLibs.mayaLibs import hierarchy_opt


class check_topology(BaseCheck):

    def run(self):
        context = pipeFile.PathDetails.parse_path()
        if context.asset_type in ["Environment"]:
            self.pass_check(u"场景资产不需要检查此项。")
            return
        mdl_topology = self.get_error_topology()
        if isinstance(mdl_topology, tuple):
            if all(mdl_topology):
                print "*"*100
                print "\n\n"
                print "increase:\n %s" % "\n".join(mdl_topology[0])
                print "\n\n"
                print "decrease:\n %s" % "\n".join(mdl_topology[1])
                print "\n\n"
                print "*"*100
                self.fail_check(u"层级结构与模型不一致")
                return
        elif isinstance(mdl_topology, list):
            if mdl_topology:
                print "*"*100
                print "\n\n"
                print "changed: \n%s" % "\n".join(mdl_topology)
                print "\n\n"
                print "*"*100
                self.error_list = mdl_topology
                self.fail_check(u"有些模型的点线面被修改")
            else:
                self.pass_check(u"拓扑结构与模型一致")
        else:
            self.warning_check(u"模型的拓扑文件不存在")

    @staticmethod
    def get_error_topology():
        model_name = get_model_name.get_model_name()
        # reference_file = mc.referenceQuery(model_name, filename=1, withoutCopyNumber=1)
        context = pipeFile.PathDetails.parse_path()
        project = context.project
        entity_type = context.entity_type
        asset_type = context.asset_type
        asset_name = context.asset_name
        HighMdl_file = pipeFile.get_task_publish_file(project, entity_type, asset_type, asset_name, "HighMdl", "HighMdl")
        context = pipeFile.PathDetails.parse_path(HighMdl_file)
        topology_path = context.topology_path
        if not os.path.isfile(topology_path):
            return
        ho = hierarchy_opt.HierarchyOpt(model_name)
        increase, decrease = ho.compare_hierarchy(topology_path)
        if all((increase, decrease)):
            return increase, decrease
        else:
            change_list = ho.compare_topology(topology_path)
            return change_list
