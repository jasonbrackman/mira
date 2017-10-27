# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import Project


class Toolkit(object):
    def __init__(self, project):
        self.project = project
        self.tk_obj = self.get_tk()

    def get_tk(self):
        """
        get the toolkit instance
        :return: database instance
        """
        database = Project(self.project).data_base
        if database == "shotgun":
            from miraLibs.sgLibs import Tk
            tk = Tk.Tk(self.project)
        elif database == "strack":
            tk = None  # todo add strack api methods
        else:
            tk = None
        return tk
