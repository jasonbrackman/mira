# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
import get_all_lights


def delete_all_lights():
    logger = logging.getLogger(__name__)
    all_lights = get_all_lights.get_all_lights()
    all_lights = [mc.listRelatives(light, parent=1) for light in all_lights]
    if not all_lights:
        return
    for light in all_lights:
        try:
            mc.delete(light)
        except:
            logger.warning("%s can not be deleted." % light)
