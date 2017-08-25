# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def run(self):
        self.error_list = self.get_unknown_nodes()
        if self.error_list:
            self.fail_check("Unknown nodes exist.")
        else:
            self.pass_check("No unknown nodes exist.")

    @staticmethod
    def get_unknown_nodes():
        unknown_nodes = mc.ls(type="unknown")
        return unknown_nodes

    def auto_solve(self):
        unknown_nodes = self.get_unknown_nodes()
        for node in unknown_nodes:
            try:
                mc.lockNode(node, l=0)
                mc.delete(node)
            except:pass
        self.error_list = self.get_unknown_nodes()
        if self.error_list:
            self.fail_check("There are some unknown can not be deleted.")
        else:
            self.pass_check("All unknown nodes has been deleted.")
