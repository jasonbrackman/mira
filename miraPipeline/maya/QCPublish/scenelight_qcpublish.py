# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.backup import backup
from miraLibs.mayaLibs import get_scene_name


def scenelight_qcpublish():
    logger = logging.getLogger(__name__)
    # copy to QCPublish path
    obj = pipeFile.PathDetails.parse_path()
    project = obj.project
    QCPublish_path = obj.QCPublish_path
    scene_name = get_scene_name.get_scene_name()
    backup.backup(project, scene_name)
    Copy.copy(scene_name, QCPublish_path)
    logger.info("copy %s >> %s" % (scene_name, QCPublish_path))
