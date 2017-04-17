# -*- coding: utf-8 -*-


def get_task_name(obj):
    if obj.entity_type == "Asset":
        task_name = "%s_%s_%s" % (obj.asset_name, obj.step, obj.task)
    else:
        task_name = "%s_%s_%s_%s" % (obj.sequence, obj.shot, obj.step, obj.task)
    return task_name
