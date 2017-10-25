# -*- coding: utf-8 -*-
import nuke
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile


class Check(BaseCheck):

    def __init__(self):
        super(Check, self).__init__()
        context = pipeFile.PathDetails.parse_path()
        self.render_path = context.render_output

    def run(self):
        write_nodes = [node["name"].getValue() for node in nuke.allNodes("Write")]
        if "Final_Render" in write_nodes:
            self.pass_check(u"Final_Render节点存在")
        else:
            self.fail_check(u"Final_Render节点不存在")

    def create_write_node(self):
        write_node = nuke.nodes.Write(name="Final_Render", file=self.render_path, postage_stamp=True, file_type=10)
        write_node.knob("datatype").setValue(1)

    def auto_solve(self):
        self.create_write_node()
        self.pass_check(u"Write节点已创建")
