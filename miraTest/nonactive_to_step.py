# -*- coding: utf-8 -*-
import shutil
import os
from miraLibs.stLibs import get_standalone_st
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import copytree


def do_it():
    st = get_standalone_st.get_standalone_st()
    nonactive_tasks = st.task.select('name=Nonactive', ["item_id", "step_id", "name"])
    assets = list()
    info = list()
    for nonactive_task in nonactive_tasks:
        print nonactive_task
        step_id = nonactive_task.get("step_id")
        item_id = nonactive_task.get("item_id")
        step = st.step.find("id=%s" % step_id)
        item = st.asset.find("id=%s" % item_id)
        step_name = step.get("name")
        item_name = item.get("name")
        if item_name == "TdTest":
            continue
        category_id = item.get("category_id")
        if category_id != 4:
            continue
        print item_name, step_name
        assets.append(item_name)
        info.append([item_name, step_name])
        entity_work_area_dir = pipeFile.get_entity_dir("SnowKidTest", "Asset", "workarea", "Prop", item_name)
        work_step_dir = os.path.join(entity_work_area_dir, step_name)
        rename_file(work_step_dir, step_name)
        entity_publish_area_dir = pipeFile.get_entity_dir("SnowKidTest", "Asset", "publish", "Prop", item_name)
        publish_step_dir = os.path.join(entity_publish_area_dir, step_name)
        rename_file(publish_step_dir, step_name)
        st.task.update(nonactive_task.get("id"), {"name": step_name})


def rename_file(step_dir, step_name):
    step_dir = step_dir.replace("\\", "/")
    if not step_dir or not os.path.isdir(step_dir):
        return
    for root, dirs, files in os.walk(step_dir):
        if not dirs:
            for f in files:
                if "Nonactive" in f:
                    file_name = os.path.join(root, f)
                    new_file_name = os.path.join(root, f.replace("Nonactive", step_name))
                    os.rename(file_name, new_file_name)
    nonactive_dir = os.path.join(step_dir, "Nonactive").replace("\\", "/")
    task_dir = os.path.join(step_dir, step_name).replace("\\", "/")
    if not os.path.isdir(nonactive_dir):
        return
    copytree.copytree(nonactive_dir, task_dir)
    shutil.rmtree(nonactive_dir)
    print "finish remove %s" % nonactive_dir


if __name__ == "__main__":
    do_it()



