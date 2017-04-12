# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import pipeFile


def get_model_name(context="model"):
    obj = pipeFile.PathDetails.parse_path()
    asset_name = obj.asset_name
    asset_type_short_name = obj.asset_type_short_name
    model_name = None
    if context == "model":
        model_name = "%s_%s_MODEL" % (asset_type_short_name, asset_name)
    elif context == "rig":
        model_name = "%s_%s_ROOT" % (asset_type_short_name, asset_name)
    return model_name
