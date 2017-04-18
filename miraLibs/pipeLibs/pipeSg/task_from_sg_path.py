# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import pipeFile


def task_from_sg_path(sg, path):
    obj = pipeFile.PathDetails.parse_path(path)
    entity_type = obj.entity_type
    step = obj.step
    task = obj.task
    if entity_type == "Asset":
        asset_type_or_sequence = obj.asset_type
        asset_or_shot = obj.asset_name
    else:
        asset_type_or_sequence = obj.sequence
        asset_or_shot = obj.shot
    task_info = sg.get_current_task(entity_type, asset_type_or_sequence, asset_or_shot, step, task)
    return task_info
