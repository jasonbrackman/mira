# -*- coding: utf-8 -*-
from get_tk_object import get_tk_object


class Tk(object):
    def __init__(self, project):
        self.project = project
        self.tk = get_tk_object(self.project)

    def get_context_from_path(self, path):
        context = self.tk.context_from_path(path)
        return context

    def get_task_from_path(self, path):
        context = self.get_context_from_path(path)
        return context.task
