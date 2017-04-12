# -*- coding: utf-8 -*-
import maya.cmds as mc
import logging


def delete_models(models):
    logger = logging.getLogger(__name__)
    if isinstance(models, basestring):
        models = [models]
    for model in models:
        is_locked = mc.lockNode(model, q=1, l=1)[0]
        if is_locked:
            mc.lockNode(model, l=0)
        try:
            mc.delete(model)
        except Exception as e:
            logger.warning(str(e))
