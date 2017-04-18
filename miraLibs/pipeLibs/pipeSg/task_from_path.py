# -*- coding: utf-8 -*-
from task_from_sg_path import task_from_sg_path
from miraLibs.sgLibs import Sg
from miraLibs.pipeLibs import pipeFile


def task_from_path(path):
    obj = pipeFile.PathDetails.parse_path(path)
    project = obj.project
    sg = Sg.Sg(project)
    task = task_from_sg_path(sg, path)
    return task
