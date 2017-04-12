# -*- coding: utf-8 -*-
import os
import re
from copy import copy
from get_engine import get_engine


class MayaTexExporter(object):
    def __init__(self, tex_dir):
        self.tex_dir = tex_dir

    @staticmethod
    def maya_get_texture_real_path(texture):
        real_texture = list()
        if "<udim>" in texture or "<UDIM>" in texture:
            texture_dir, texture_base_name = os.path.split(texture)
            pattern = texture_base_name.replace("<udim>", "\d{4}")
            pattern = pattern.replace("<UDIM>", "\d{4}")
            for i in os.listdir(texture_dir):
                if re.match(pattern, i):
                    full_name = os.path.join(texture_dir, i).replace("\\", "/")
                    real_texture.append(full_name)
        elif os.path.isfile(texture):
            real_texture.append(texture)
        else:
            print "%s is not an exist file." % texture
        return real_texture

    def export(self):
        import maya.cmds as mc
        import maya.mel as mel
        mel.eval("MLdeleteUnused;")
        file_nodes = mc.ls(type="file")
        if not file_nodes:
            return
        textures = list()
        for file_node in file_nodes:
            texture = mc.getAttr("%s.computedFileTextureNamePattern" % file_node)
            if not texture:
                continue
            tex_real_path = self.maya_get_texture_real_path(texture)
            textures.extend(tex_real_path)
        if not textures:
            return
        for texture in textures:
            base_name = os.path.basename(texture)
            new_texture = os.path.join(self.tex_dir, base_name).replace("\\", "/")
            copy(texture, new_texture)


class TexExporter(object):
    def __init__(self, tex_dir):
        self.engine = get_engine()
        self.tex_dir = tex_dir

    def export(self):
        if self.engine == "maya":
            exporter = MayaTexExporter(self.tex_dir)
        elif self.engine == "houdini":
            print "add houdini export texture method"
            # todo add houdini export texture method.
            pass
        else:
            pass
        exporter.export()


