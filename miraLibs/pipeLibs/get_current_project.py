# -*- coding: utf-8 -*-
import logging
import sys
import pipeGlobal
from miraLibs.pipeLibs import pipeFile, pipeHistory


def get_current_project():
    logger = logging.getLogger(__name__)
    run_app = sys.executable
    current_project = None
    if run_app.endswith("maya.exe"):
        try:
            context = pipeFile.PathDetails.parse_path()
            current_project = context.project
            logger.info("Get project from scene name.")
        except:
            from miraLibs.mayaLibs import get_maya_globals
            maya_globals = get_maya_globals.get_maya_globals()
            if maya_globals.exists("currentProject"):
                current_project = maya_globals.get("currentProject").get()
                logger.info("Get project from maya globals.")
    if not current_project:
        current_project = pipeHistory.get("currentProject")
        if current_project:
            logger.info("Get project from history.")
        else:
            current_project = pipeGlobal.current_project
            logger.info("Get project from configuration.")
    if current_project and current_project not in pipeGlobal.projects:
        current_project = pipeGlobal.current_project
        logger.info("Get project from configuration.")
    return current_project
