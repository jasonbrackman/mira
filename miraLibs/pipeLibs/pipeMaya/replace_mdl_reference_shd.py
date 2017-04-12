# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import replace_reference


def replace_mdl_reference_shd():
    """
    replace mdl reference to shd.
    """
    logger = logging.getLogger(__name__)
    transforms = mc.listRelatives("env", ad=1, c=1, type="transform")
    ref_files = list()
    for transform in transforms:
        if mc.referenceQuery(transform, inr=1) and transform.endswith("_MODEL"):
            ref_file = mc.referenceQuery(transform, filename=1)
            ref_files.append(ref_file)
    logger.info("reference files: %s" % ref_files)
    if not ref_files:
        return
    for ref_file in ref_files:
        obj = pipeFile.PathDetails().parse_path(ref_file)
        if not obj:
            continue
        project = obj.project
        asset_type = obj.asset_type
        asset_name = obj.asset_name
        ref_node = mc.referenceQuery(ref_file, rfn=1)
        logger.info("reference node: %s" % ref_node)
        shd_publish_path = pipeFile.get_asset_step_publish_file(asset_type, asset_name, "shd", project)
        if shd_publish_path:
            replace_reference.replace_reference(ref_node, shd_publish_path)
        else:
            logger.error("%s's shd publish file is not exist." % asset_name)


if __name__ == "__main__":
    replace_mdl_reference_shd()
