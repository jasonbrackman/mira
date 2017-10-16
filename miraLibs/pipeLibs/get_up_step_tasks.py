# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import Step
from miraLibs.stLibs import St


def get_up_step_tasks(project, entity_type, asset_type_sequence, asset_name_shot, step):
    up_steps = Step(project, step).up_step
    if not up_steps:
        return
    st = St.St(project)
    all_up_step_task = list()
    for up_step in up_steps:
        if up_step == "Set":
            asset_name_shot = "%s_%s" % (asset_type_sequence, "c000")
        tasks = st.get_task(entity_type, asset_type_sequence, asset_name_shot, up_step)
        all_up_step_task.extend(tasks)
    return all_up_step_task
