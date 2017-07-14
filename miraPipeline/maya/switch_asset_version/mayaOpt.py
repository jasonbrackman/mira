# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import replace_reference


def get_all_ref():
    all_ref = mc.ls(type='reference')
    all_ref = [ref for ref in all_ref if 'sharedReferenceNode' not in ref]
    return all_ref


def get_ref_files():
    ref_nodes = get_all_ref()
    ref_files = [mc.referenceQuery(ref_node, filename=1) for ref_node in ref_nodes]
    return ref_files


def get_project_ref_files():
    ref_files = get_ref_files()
    if not ref_files:
        return
    project_ref_files = [ref_file for ref_file in ref_files if pipeFile.PathDetails.parse_path(ref_file)]
    return project_ref_files


def get_asset_list():
    project_ref_files = get_project_ref_files()
    if not project_ref_files:
        return
    asset_list = list()
    for ref_file in project_ref_files:
        nodes = mc.referenceQuery(ref_file, dagPath=1, nodes=1)
        if not nodes:
            continue
        group_name = nodes[0]
        obj = pipeFile.PathDetails.parse_path(ref_file)
        step = obj.step
        task = obj.task
        asset_type = obj.asset_type
        asset_type_short_name = obj.asset_type_short_name
        asset_name = obj.asset_name
        project = obj.project
        image_path = pipeFile.get_task_workImage_file(project, "Asset", asset_type, asset_name, step, task)
        dst_path = os.path.dirname(ref_file)
        asset_list.append([group_name, image_path, dst_path, asset_type_short_name])
    return asset_list


def replace(group_name, new_path):
    ref_node = mc.referenceQuery(group_name, referenceNode=1)
    replace_reference.replace_reference(ref_node, new_path)


def select(objects):
    mc.select(objects, r=1)
