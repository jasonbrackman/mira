# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import import_load_remove_unload_ref, open_file, save_as, \
    quit_maya, export_selected, delete_layer
from miraLibs.pipeLibs import pipeFile


def main(file_name):
    logger = logging.getLogger("hair publish")
    open_file.open_file(file_name)
    obj = pipeFile.PathDetails.parse_path(file_name)
    asset_type_short_name = obj.asset_type_short_name
    asset_name = obj.asset_name
    publish_path = obj.publish_path
    hair_path = obj.hair_path
    yeti_group = "%s_%s_yetiNode" % (asset_type_short_name, asset_name)
    # import mdl reference
    import_load_remove_unload_ref.import_load_remove_unload_ref()
    # export yeti group to _hair group
    delete_layer.delete_layer()
    mc.select(yeti_group, r=1)
    export_selected.export_selected(hair_path)
    logger.info("export yeti node to _hair done.")
    mc.delete(yeti_group)
    # save to publish path
    save_as.save_as(publish_path)
    # quit maya
    quit_maya.quit_maya()
