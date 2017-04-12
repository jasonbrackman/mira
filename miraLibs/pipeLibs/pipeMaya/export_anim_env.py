# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import export_selected
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import replace_mdl_reference_shd


def export_anim_env(env_path):
    """
    export animation environment for lighting.
    :param env_path:
    :return:
    """
    if not mc.objExists("env"):
        return
    if not mc.listRelatives("env", c=1):
        return
    replace_mdl_reference_shd.replace_mdl_reference_shd()
    mc.select("env", r=1)
    export_selected.export_selected(env_path, pr_flag=True)





