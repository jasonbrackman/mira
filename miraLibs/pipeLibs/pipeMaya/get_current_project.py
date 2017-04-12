# -*- coding: utf-8 -*-
import logging
import sys
from miraLibs.pipeLibs import pipeFile, pipeMira, pipeHistory
from miraLibs.mayaLibs import get_maya_globals


def get_current_project():
    logger = logging.getLogger(__name__)
    run_app = sys.executable
    current_project = None
    if run_app.endswith("maya.exe"):
        obj = pipeFile.PathDetails.parse_path()
        if obj:
            current_project = obj.project
            logger.info("Get project from scene name.")
        else:
            maya_globals = get_maya_globals.get_maya_globals()
            if maya_globals.exists("currentProject"):
                current_project = maya_globals.get("currentProject").get()
                logger.info("Get project from maya globals.")
    if not current_project:
        current_project = pipeHistory.get("currentProject")
        if current_project:
            logger.info("Get project from history.")
        else:
            current_project = pipeMira.get_current_project()
            logger.info("Get project from configuration.")
    return current_project
