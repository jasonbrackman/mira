# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc


def remove_reference_by_group(group_name):
    logger = logging.getLogger(__name__)
    if not mc.objExists(group_name):
        logger.warning("%s does not exist." % group_name)
        return
    is_reference = mc.referenceQuery(group_name, isNodeReferenced=1)
    if not is_reference:
        logger.info("%s is not reference." % group_name)
        return
    ref_file = mc.referenceQuery(group_name, filename=1)
    try:
        mc.file(ref_file, rr=1)
    except RuntimeError as e:
        logger.error(str(e))
