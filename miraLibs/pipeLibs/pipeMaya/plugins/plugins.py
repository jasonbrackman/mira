# -*- coding: utf-8 -*-
import logging
import pipeGlobal
import miraLibs.pyLibs.yml_operation as yml
import miraLibs.pyLibs.join_path as join_path
from miraLibs.mayaLibs import load_plugin, unload_plugin

logger = logging.getLogger(__name__)
conf_dir = pipeGlobal.conf_dir


def get_plugin_conf_data():
    plugin_conf_path = join_path.join_path2(conf_dir, "plugins.yml")
    yml_data = yml.get_yaml_data(plugin_conf_path)
    return yml_data


def load_plugins():
    plugins = get_plugin_conf_data().get("load")
    if not plugins:
        return
    logger.info("Load plugins: %s" % "; ".join(plugins))
    for plugin in plugins:
        try:
            load_plugin.load_plugin(plugin)
            logger.info("Load plugin %s done." % plugin)
        except RuntimeError as e:
            logger.error(str(e))


def unload_plugins():
    plugins = get_plugin_conf_data().get("unload")
    if not plugins:
        return
    for plugin in plugins:
        try:
            unload_plugin.unload_plugin(plugin)
            logger.info("unload plugin %s done." % plugin)
        except RuntimeError as e:
            logger.error(str(e))
