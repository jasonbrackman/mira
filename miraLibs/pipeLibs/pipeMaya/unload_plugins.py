# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeMira
from miraLibs.mayaLibs import unload_plugin


def unload_plugins():
    logger = logging.getLogger(__name__)
    plugins = pipeMira.get_unload_plugins()
    if not plugins:
        return
    for plugin in plugins:
        try:
            unload_plugin.unload_plugin(plugin)
            logger.info("unload plugin %s done." % plugin)
        except RuntimeError as e:
            logger.error(str(e))
