# -*- coding: utf-8 -*-
from miraLibs.sgLibs import Tk
from miraLibs.pipeLibs import pipeMira


class Toolkit(object):
    def __init__(self, project):
        self.project = project
        self.tk_obj = self.get_tk()

    def get_tk(self):
        """
        get the toolkit instance
        :return: database instance
        """
        database = pipeMira.get_site_value(self.project, "database")
        if database == "shotgun":
            tk = Tk.Tk(self.project)
        elif database == "strack":
            tk = None  # todo add strack api methods
        else:
            tk = None
        return tk