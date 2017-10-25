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
        write_path = self.get_write_path()
        if self.render_path == write_path:
            self.pass_check(u"路径设置正确")
        else:
            self.fail_check(u"Write节点输出路径设置错误")

    def get_write_path(self):
        write_node = nuke.toNode("Final_Render")
        file_name = write_node["file"].getValue()
        return file_name

    def auto_solve(self):
        write_node = nuke.toNode("Final_Render")
        write_node["file"].setValue(self.render_path)
        self.pass_check(u"输出路径设置正确")
