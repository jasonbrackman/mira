# -*- coding: utf-8 -*-
import time
import maya.cmds as mc
from miraLibs.pipeLibs.pipeDb import sql_api


def publish_to_db(project):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    task_id = int(mc.getAttr("ROOT.task_id"))
    db = sql_api.SqlApi(project)
    arg_dict = {'taskId': task_id, 'taskEndDate': current_time}
    db.releaseTask(arg_dict)
