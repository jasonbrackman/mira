# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile, pipeMira
import miraLibs.mayaLibs.HeadsUpDisplay as hu
import miraLibs.mayaLibs.get_maya_globals as get_maya_globals


def get_company():
    company = pipeMira.get_company()
    return company


def get_project():
    context = pipeFile.PathDetails.parse_path()
    if context:
        return context.project
    else:
        return ""


def get_resolution():
    current_project = get_project()
    if current_project:
        resolution = pipeMira.get_resolution(current_project)
        resolution = "*".join([str(i) for i in resolution])
    else:
        resolution = ""
    return resolution


def get_task_name():
    try:
        context = pipeFile.PathDetails.parse_path()
        if context.entity_type == "Shot":
            return "_".join([context.sequence, context.shot, context.step, context.task])
        else:
            return "_".join([context.asset_name, context.step, context.task])
    except:
        return ""


def get_frame_range():
    start = int(mc.playbackOptions(q=1, min=1))
    end = int(mc.playbackOptions(q=1, max=1))
    frame_range = "%s-%s" % (start, end)
    return frame_range


def get_hud_object():
    maya_globals = get_maya_globals.get_maya_globals()
    if "hud" not in maya_globals.keys():
        hud_obj = hu.HeadsUpDisplay()
        maya_globals.add(hud=hud_obj)
    return maya_globals.get("hud")
