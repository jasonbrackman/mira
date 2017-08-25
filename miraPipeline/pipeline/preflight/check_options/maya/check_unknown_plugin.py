# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def run(self):
        self.error_list = self.get_unknown_plugins()
        if self.error_list:
            self.fail_check("Unknown plugins exist.")
        else:
            self.pass_check("No unknown plugins exist.")

    @staticmethod
    def get_unknown_plugins():
        return mc.unknownPlugin(q=True, list=True)

    def auto_solve(self):
        unknown_plugins = self.get_unknown_plugins()
        for plugin in unknown_plugins:
            try:
                mc.unknownPlugin(plugin, remove=True)
            except:pass
        self.error_list = self.get_unknown_plugins()
        if self.error_list:
            self.fail_check("There are some unknown can not be deleted.")
        else:
            self.pass_check("All unknown nodes has been deleted.")
