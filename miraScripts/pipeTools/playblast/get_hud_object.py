# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import pipeMira, pipeFile
import miraLibs.mayaLibs.HeadsUpDisplay as hud
import miraLibs.mayaLibs.get_maya_globals as get_maya_globals


def get_company():
    company = pipeMira.get_company()
    return company


def get_project():
    try:
        obj = pipeFile.PathDetails.parse_path()
        return obj.project
    except:
        return ""


def get_shot_name():
    try:
        obj = pipeFile.PathDetails.parse_path()
        if obj.path_type == "shot":
            return "_".join([obj.seq, obj.shot])
        else:
            return obj.asset_name
    except:
        return ""


def get_hud_object():
    maya_globals = get_maya_globals.get_maya_globals()
    if "hud" not in maya_globals.keys():
        company_name = get_company()
        project_name = get_project()
        shot_name = get_shot_name()
        hud_obj = hud.HeadsUpDisplay(company_name, project_name, shot_name)
        maya_globals.add(hud=hud_obj)
    return maya_globals.get("hud")


if __name__ == "__main__":
    pass
