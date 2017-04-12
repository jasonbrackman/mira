# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import rename_shape
from miraLibs.pipeLibs.pipeMaya import get_model_name


def rename_pipeline_shape():
    model_group = get_model_name.get_model_name()
    mc.select(model_group, r=1)
    if rename_shape.rename_shape():
        return True
    else:
        return False
