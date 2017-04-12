import os
import logging

# Local modules
from get_tk_object import get_tk_object
from PublishPathCalculator import PublishPathCalculator


def get_file_base_dict(file_name):

    name_parts = file_name.split("_")
    if len(name_parts) not in [4, 5]:
        return
    elif len(name_parts) == 4:
        entity_name = name_parts[1]
    else:
        entity_name = "%s_%s" % (name_parts[1],name_parts[2])
    task_type = name_parts[-2]    
    logging.debug("entity_name:%s , task_type:%s"% (entity_name, task_type))
    tk = get_tk_object()
    path_calculator = PublishPathCalculator(tk)
    file_path = path_calculator.calculat(entity_name, task_type)
    # get base dict
    return _get_base_dict(file_path, tk)
    
    
def _get_base_dict(file_path, tk):
    baseDict = {'show' : None,
                'showShortname' : None,
                'fileFormat_need' : None,        # "mayaAscii" or "mayaBinary"
                'sequence' : None, 'shot' : None,
                'category':None, 'asset':None,
                'area':None,        # publish area
                'taskName':None, 'taskType':None,
                'version':None,
                'fileExt':None,
                'hasTk':True,
                'highMode':'h',     # always "h"
                'projBase':None     # always "None"
                }
    try:
        task_context = tk.context_from_path(file_path)
        # -show and showShortname
        baseDict["show"] = baseDict["showShortname"] = task_context.project["name"]
        # -fileFormat_need
        need_ext = os.path.splitext(file_path)[-1]
        if need_ext == ".mb":
            baseDict["fileFormat_need"] = "mayaBinary"
        elif need_ext == ".ma":
            baseDict["fileFormat_need"] = "mayaAscii"
        else:
            pass    # not a maya file
        # -sequence, shot or category, asset
        if task_context.entity["type"] == "Shot":
            baseDict["sequence"], baseDict["shot"] = task_context.entity["name"].split("_")
        else:
            baseDict["asset"] = task_context.entity["name"]
            asset_id = task_context.entity["id"]
            baseDict["category"] = tk.shotgun.find_one("Asset",[["id","is",asset_id]],["sg_asset_type"])["sg_asset_type"]
        # -area
        baseDict["area"] = os.path.dirname(file_path)
        # -taskName
        task_id = task_context.task["id"]
        task_dict = tk.shotgun.find_one("Task",[["id","is",task_id]],["sg_task_part_name"])
        baseDict["taskName"] = task_dict["sg_task_part_name"]
        # -taskType
        baseDict["taskType"] = task_context.additional_entities[0]["name"]
        # -version and fileExt
        postfix = file_path.split("_")[-1]
        baseDict["version"], baseDict["fileExt"] = postfix.split(".")
    except:
        logging.warning("Some thing wrong during getting values...")
    finally:
        return baseDict
    
    
if __name__ == "__main__":
    file_name = r"df_YoungDouFu_mdl_v012.mb"
    print get_file_base_dict(file_name)
    file_name = r"df_999_000_pv_v001.mb"
    print get_file_base_dict(file_name)
