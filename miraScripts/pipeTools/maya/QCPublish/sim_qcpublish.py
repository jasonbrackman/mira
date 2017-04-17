# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_scene_name
from miraScripts.pipeTools.maya.playblast import playblast_shot


def sim_qcpublish():
    logger = logging.getLogger(__name__)
    # playblast
    playblast_shot.playblast_shot()
    # copy to QCPublish path
    obj = pipeFile.PathDetails.parse_path()
    work_path = obj.work_path
    scene_name = get_scene_name.get_scene_name()
    if Copy.copy(scene_name, work_path):
        logger.info("copy %s >> %s" % (scene_name, work_path))
    else:
        raise RuntimeError("copy to work path error.")
