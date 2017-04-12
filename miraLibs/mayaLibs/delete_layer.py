# -*- coding: utf-8 -*-
import maya.cmds as mc


def delete_display_layer():
    layers = mc.ls(type="displayLayer")
    layers = [layer for layer in layers if "defaultLayer" not in layer]
    if not layers:
        return
    mc.delete(layers)


def delete_render_layer():
    layers = mc.ls(type="renderLayer")
    layers = [layer for layer in layers if "defaultRenderLayer" not in layer]
    if not layers:
        return
    for layer in layers:
        mc.editRenderLayerGlobals(crl="defaultRenderLayer")
        mc.delete(layer)


def delete_anim_layer():
    layers = mc.ls(type="animLayer")
    if not layers:
        return
    mc.delete(layers)


def delete_layer():
    delete_display_layer()
    delete_render_layer()
    delete_anim_layer()
