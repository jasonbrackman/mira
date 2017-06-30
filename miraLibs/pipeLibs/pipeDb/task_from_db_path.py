# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import pipeFile


def task_from_db_path(db, path):
    obj = pipeFile.PathDetails.parse_path(path)
    entity_type = obj.entity_type
    step = obj.step
    task = obj.task
    if entity_type in ["Asset"]:
        asset_type_or_sequence = obj.asset_type
        asset_or_shot = obj.asset_name
    else:
        asset_type_or_sequence = obj.sequence
        asset_or_shot = obj.shot
    task_info = db.get_current_task(entity_type, asset_type_or_sequence, asset_or_shot, step, task)
    return task_info


if __name__ == "__main__":
    from miraLibs.stLibs import St
    db = St.St("SnowKidTest")
    print task_from_db_path(db, r"D:\SnowKidTest\workarea\assets\Prop\TdTest\MidMdl\MidMdl\_workarea\maya\SnowKidTest_TdTest_MidMdl_MidMdl_v000_e000.ma")