# -*- coding: utf-8 -*-
import task_from_path
from miraLibs.dbLibs import toolkit
from miraLibs.pipeLibs import pipeFile


def create_filesystem_structure(path, engine="tk-maya"):
    task_info = task_from_path.task_from_path(path)
    if not task_info:
        return
    obj = pipeFile.PathDetails.parse_path(path)
    project = obj.project
    tk = toolkit.Toolkit(project).tk_obj
    task_id = task_info["id"]
    tk.create_filesystem_structure(task_id, engine=engine)
