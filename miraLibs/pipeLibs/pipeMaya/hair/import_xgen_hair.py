import os
import maya.cmds as mc
from miraLibs.mayaLibs import Xgen
from miraLibs.pyLibs import json_operation
from miraLibs.log import Logger


logger = Logger(__name__)


def import_sculp_cache(context, namespace):
    cache_path = context.abc_cache_path
    if not namespace:
        namespace = ":"
    mc.file(cache_path, i=1, namespace=namespace, f=1)


def import_palette(context, namespace):
    xgen_file_path = context.hair_path
    delta_path = context.delta_path
    xgen = Xgen.Xgen()
    xgen.import_palette(xgen_file_path, delta_path, namespace)


def import_shader(context):
    shd_path = context.shd_path
    if os.path.isfile(shd_path):
        mc.file(shd_path, i=1)


def assign_shader(context, namespace):
    connection_path = context.connection_path
    if os.path.isfile(connection_path):
        data = json_operation.get_json_data(connection_path)
        for description in data:
            sg = data.get(description)
            try:
                if namespace != ":":
                    description = "%s:%s" % (namespace, description)
                mc.sets(description, fe=sg)
            except:
                logger.info("Can't assign shader %s --> %s" % (description, sg))


def import_xgen_hair(context, namespace):
    cache_path = context.abc_cache_path
    xgen_file_path = context.hair_path
    delta_path = context.delta_path
    print cache_path, xgen_file_path, delta_path
    if not all((os.path.isfile(cache_path), os.path.isfile(xgen_file_path), os.path.isfile(delta_path))):
        logger.info("Hair cache .xgen .xgd file not exist.")
        return
    import_sculp_cache(context, namespace)
    logger.info("Import sculp cache done.")
    import_palette(context, namespace)
    logger.info("Import palette done.")
    import_shader(context)
    logger.info("Import shader done.")
    assign_shader(context, namespace)
    logger.info("Assign shader done.")
