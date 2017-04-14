# -*- coding: utf-8 -*-
import os
from copy import copy
from get_engine import get_engine


class MayaShdExporter(object):
    def __init__(self, shd_path):
        self.shd_path = shd_path

    @staticmethod
    def delete_display_layer():
        import maya.cmds as mc
        layers = mc.ls(type="displayLayer")
        layers = [layer for layer in layers if "defaultLayer" not in layer]
        if not layers:
            return
        mc.delete(layers)

    @staticmethod
    def delete_render_layer():
        import maya.cmds as mc
        layers = mc.ls(type="renderLayer")
        layers = [layer for layer in layers if "defaultRenderLayer" not in layer]
        if not layers:
            return
        for layer in layers:
            mc.editRenderLayerGlobals(crl="defaultRenderLayer")
            mc.delete(layer)

    @staticmethod
    def delete_anim_layer():
        import maya.cmds as mc
        layers = mc.ls(type="animLayer")
        if not layers:
            return
        mc.delete(layers)

    def delete_layer(self):
        self.delete_display_layer()
        self.delete_render_layer()
        self.delete_anim_layer()

    def export(self):
        import maya.cmds as mc
        self.delete_layer()
        mc.file(save=1, f=1)
        scene_name = mc.file(q=1, sn=1)
        file_ext = os.path.splitext(scene_name)[1]
        shd_ext = os.path.splitext(self.shd_path)[1]
        if file_ext == shd_ext:
            copy(scene_name, self.shd_path)
        else:
            shd_path = os.path.splitext(self.shd_path)[0] + file_ext
            print shd_path
            copy(scene_name, shd_path)


class ShdExporter(object):
    def __init__(self, shd_path):
        self.engine = get_engine()
        self.shd_path = shd_path

    def export(self):
        if self.engine == "maya":
            exporter = MayaShdExporter(self.shd_path)
        elif self.engine == "houdini":
            print "add houdini export texture method"
            # todo add houdini export texture method.
            pass
        else:
            pass
        exporter.export()
