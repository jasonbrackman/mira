# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import pipeFile


def get_model_name(typ="model"):
    context = pipeFile.PathDetails.parse_path()
    if not context:
        print "get_model_name: context is None"
        return
    asset_name = context.asset_name
    asset_type_short_name = context.asset_type_short_name
    model_name = None
    if typ == "model":
        model_name = "%s_%s_MODEL" % (asset_type_short_name, asset_name)
    elif typ == "rig":
        model_name = "%s_%s_ROOT" % (asset_type_short_name, asset_name)
    elif typ == "AD":
        model_name = "%s_%s_AD" % (asset_type_short_name, asset_name)
    return model_name
