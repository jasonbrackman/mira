# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_scene_name


def main():
    logger = logging.getLogger(__name__)
    # copy to QCPublish path
    context = pipeFile.PathDetails.parse_path()
    work_path = context.work_path
    scene_name = get_scene_name.get_scene_name()
    if Copy.copy(scene_name, work_path):
        logger.info("copy %s >> %s" % (scene_name, work_path))
    else:
        raise RuntimeError("copy to work path error.")
