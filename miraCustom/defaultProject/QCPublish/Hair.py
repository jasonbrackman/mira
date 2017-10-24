# -*- coding: utf-8 -*-
import os
import logging
import tempfile
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_scene_name, open_file, save_file
from miraLibs.mayaLibs.Xgen import Xgen
from miraLibs.pyLibs import copytree, copy, join_path
from miraLibs.pipeLibs.copy import Copy


def main():
    logger = logging.getLogger(__name__)
    scene_name = get_scene_name.get_scene_name()
    context = pipeFile.PathDetails.parse_path()
    asset_name = context.asset_name
    collection_node = "%s_collection" % asset_name
    # copy scene and .xgen file to temp dir
    base_name = os.path.basename(scene_name)
    xgen_base_name = mc.getAttr("%s.xgFileName" % collection_node)
    xgen_path = join_path.join_path2(os.path.dirname(scene_name), xgen_base_name)
    temp_dir = tempfile.gettempdir()
    maya_temp_file = join_path.join_path2(temp_dir, base_name)
    xgen_temp_file = join_path.join_path2(temp_dir, xgen_base_name)
    copy.copy(scene_name, maya_temp_file)
    copy.copy(xgen_path, xgen_temp_file)
    logger.info("Copy to temp: %s" % maya_temp_file)
    # copy local xgen dir to publish.
    xgen_dir = copy_xgen_dir(context)
    logger.info("Copy xgen dir to %s" % xgen_dir)
    # set the path as abs path
    xgen = Xgen()
    xgen.set_abs_path(xgen_dir)
    save_file.save_file()
    logger.info("Set abs path done.")
    # copy to work path
    work_path = context.work_path
    Copy.copy(scene_name, work_path)
    Copy.copy(xgen_path, join_path.join_path2(os.path.dirname(work_path), xgen_base_name))
    logger.info("copy maya file and .xgen file to workarea done.")
    # copy from temp file
    copy.copy(maya_temp_file, scene_name)
    copy.copy(xgen_temp_file, xgen_path)
    # delete temp file
    os.remove(maya_temp_file)
    os.remove(xgen_temp_file)
    # open scene name
    open_file.open_file(scene_name)
    logger.info("Reopen %s" % scene_name)


def copy_xgen_dir(context):
    project_dir = os.path.dirname(mc.file(q=1, sn=1))
    local_xgen_dir = os.path.join(project_dir, "xgen").replace("\\", "/")
    xgen_dir = context.xgen_dir
    try:
        copytree.copytree(local_xgen_dir, xgen_dir)
        return xgen_dir
    except:
        raise
