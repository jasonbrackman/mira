# -*- coding: utf-8 -*-
import os
import nuke
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def __init__(self):
        super(Check, self).__init__()
        self.read_nodes = nuke.allNodes("Read")

    def run(self):
        if not self.read_nodes:
            self.warning_check("No read node exist.")
            return
        self.error_list = self.get_error_list()
        print self.error_list
        if self.error_list:
            self.fail_check("some path is invalid.")
        else:
            self.pass_check("All is right.")

    def get_error_list(self):
        error_list = list()
        read_nodes = self.read_nodes
        if read_nodes:
            for read_node in read_nodes:
                f = read_node["file"].getValue()
                if not os.path.isfile(f):
                    error_list.append(read_node["name"].getValue())
        return error_list
