import os
import maya.cmds as mc
from miraLibs.mayaLibs import Xgen, import_abc
from miraLibs.pyLibs import json_operation
from miraLibs.log import Logger


logger = Logger(__name__)


def import_sculp_cache(context):
    cache_path = context.abc_cache_path
    import_abc.import_abc(cache_path)


def import_palette(context):
    xgen_file_path = context.hair_path
    delta_path = context.delta_path
    xgen = Xgen.Xgen()
    xgen.import_palette(xgen_file_path, delta_path)


def import_shader(context):
    shd_path = context.shd_path
    if os.path.isfile(shd_path):
        mc.file(shd_path, i=1)


def assign_shader(context):
    connection_path = context.connection_path
    if os.path.isfile(connection_path):
        data = json_operation.get_json_data(connection_path)
        for description in data:
            sg = data.get(description)
            try:
                mc.sets(description, fe=sg)
            except:
                logger.info("Can't assign shader %s --> %s" % (description, sg))


def import_xgen_hair(context):
    cache_path = context.abc_cache_path
    xgen_file_path = context.hair_path
    delta_path = context.delta_path
    print cache_path, xgen_file_path, delta_path
    if not all((os.path.isfile(cache_path), os.path.isfile(xgen_file_path), os.path.isfile(delta_path))):
        logger.info("Hair cache .xgen .xgd file not exist.")
        return
    import_sculp_cache(context)
    logger.info("Import sculp cache done.")
    import_palette(context)
    logger.info("Import palette done.")
    import_shader(context)
    logger.info("Import shader done.")
    assign_shader(context)
    logger.info("Assign shader done.")
