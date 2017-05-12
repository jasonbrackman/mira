# -*- coding: utf-8 -*-
from task_from_db_path import task_from_db_path
from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs import pipeFile


def task_from_path(path):
    obj = pipeFile.PathDetails.parse_path(path)
    project = obj.project
    db = db_api.DbApi(project).db_obj
    task = task_from_db_path(db, path)
    return task
