# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.pyLibs import copy
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, export_selected
from miraLibs.pipeLibs.pipeMaya import publish
from miraLibs.pipeLibs.pipeMaya.rebuild_assembly import export_scene


def main(file_name, local):
    logger = logging.getLogger("MainLgt publish")
    if not local:
        open_file.open_file(file_name)
    # export edits
    export_scene()
    logger.info("Export edits done.")
    # delete Env
    try:
        mc.delete("Env")
    except:
        print "Can't delete Env"
    context = pipeFile.PathDetails.parse_path()
    publish.copy_image_and_video(context)
    # export Lights to _light
    mc.select("Lights", r=1)
    export_selected.export_selected(context.light_path)
    logger.info("Export Lights to %s" % context.light_path)
    # copy to publish path
    copy.copy(file_name, context.publish_path)
    logger.info("Copy to publish path")
    # quit maya
    if not local:
        quit_maya.quit_maya()
