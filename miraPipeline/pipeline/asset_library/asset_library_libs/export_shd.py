# -*- coding: utf-8 -*-
import os
from get_engine import get_engine
try:
    from maya_undo import undo
except:pass


class MayaShdExporter(object):
    def __init__(self, shd_path, tex_dir):
        self.shd_path = shd_path
        self.tex_dir = tex_dir

    @undo
    def set_file_texture_name(self):
        from maya_get_file_nodes import maya_get_file_nodes
        import maya.cmds as mc
        file_nodes = maya_get_file_nodes()
        if not file_nodes:
            return
        for file_node in file_nodes:
            file_texture = mc.getAttr("%s.fileTextureName" % file_node)
            base_name = os.path.basename(file_texture)
            new_texture = os.path.join(self.tex_dir, base_name).replace("\\", "/")
            print new_texture
            mc.setAttr("%s.fileTextureName" % file_node, new_texture, type="string")

    def export(self):
        import maya.cmds as mc
        self.set_file_texture_name()
        # export current select to shd path
        shd_dir = os.path.dirname(self.shd_path)
        if not os.path.isdir(shd_dir):
            os.makedirs(shd_dir)
        mc.file(self.shd_path, exportSelected=1, type="mayaBinary", force=1, pr=1, options="v=0;")
        mc.undo()


class ShdExporter(object):
    def __init__(self, shd_path, tex_dir):
        self.engine = get_engine()
        self.shd_path = shd_path
        self.tex_dir = tex_dir

    def export(self):
        if self.engine == "maya":
            exporter = MayaShdExporter(self.shd_path, self.tex_dir)
        elif self.engine == "houdini":
            print "add houdini export texture method"
            # todo add houdini export texture method.
            pass
        else:
            pass
        exporter.export()
