# -*- coding: utf-8 -*-
import mayaOpt.cmds as mc


def get_render_layer_objects(layer):
    objects = mc.editRenderLayerMembers(layer, query=True)
    return objects
