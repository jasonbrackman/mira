# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeMira
from miraLibs.mayaLibs import load_plugin


def load_plugins():
    logger = logging.getLogger(__name__)
    plugins = pipeMira.get_load_plugins()
    if not plugins:
        return
    logger.info("Load plugins: %s" % "; ".join(plugins))
    for plugin in plugins:
        try:
            load_plugin.load_plugin(plugin)
            logger.info("Load plugin %s done." % plugin)
        except RuntimeError as e:
            logger.error(str(e))
