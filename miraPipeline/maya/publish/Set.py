# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, export_selected
from miraLibs.pipeLibs.pipeMaya import publish


def main(file_name, local):
    logger = logging.getLogger("sceneset publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    sequence = context.sequence
    publish_path = context.publish_path
    # export {sequence}_env to publish
    env_group = "%s_env" % sequence
    mc.select(env_group, r=1)
    export_selected.export_selected(publish_path)
    logger.info("Export %s to publish done." % env_group)
    # copy image and video
    publish.copy_image_and_video(context)
    # create AD file
    publish.create_shot_ad(context)
    logger.info("Create AD done.")
    # quit maya
    if not local:
        quit_maya.quit_maya()
