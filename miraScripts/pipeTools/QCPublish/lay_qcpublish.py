# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_scene_name
from miraScripts.pipeTools.playblast import playblast_lay
from miraLibs.pipeLibs.copy import Copy


def lay_qcpublish():
    logger = logging.getLogger(__name__)
    # playblast to video
    pl = playblast_lay.PlayblastLay()
    pl.playblast_lay()
    logger.info("Playblast Done.")
    # export all camera
    scene_name = get_scene_name.get_scene_name()
    obj = pipeFile.PathDetails.parse_path()
    work_path = obj.work_path
    if Copy.copy(scene_name, work_path):
        logger.info("copy %s >> %s" % (scene_name, work_path))
    else:
        raise RuntimeError("copy to work path error.")


if __name__ == "__main__":
    pass
