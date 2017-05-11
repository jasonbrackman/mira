# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_scene_name, hierarchy_opt
from miraPipeline.maya.playblast import playblast_turntable
from miraLibs.pipeLibs.pipeMaya import get_model_name


def mdl_qcpublish():
    logger = logging.getLogger(__name__)
    # copy to QCPublish path
    obj = pipeFile.PathDetails.parse_path()
    work_path = obj.work_path
    topology_path = obj.topology_path
    model_name = get_model_name.get_model_name()
    scene_name = get_scene_name.get_scene_name()
    if Copy.copy(scene_name, work_path):
        logger.info("copy %s >> %s" % (scene_name, work_path))
    else:
        raise RuntimeError("copy to work path error.")
    # write out topology
    ho = hierarchy_opt.HierarchyOpt(model_name)
    ho.write_out(topology_path)
    # playblast to video
    logger.info("Start playblasting...")
    playblast_turntable.playblast_turntable()
    logger.info("Playblast successful")


