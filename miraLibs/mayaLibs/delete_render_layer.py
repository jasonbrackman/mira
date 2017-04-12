# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc


def delete_render_layer(layer_name):
    logger = logging.getLogger(__name__)
    mc.editRenderLayerGlobals(crl="defaultRenderLayer")
    try:
        mc.delete(layer_name)
    except Exception as e:
        logger.error(str(e))
