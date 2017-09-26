import shutil
import os
import logging
import maya.cmds as mc
import xgenm as xgen
import xgenm.xgGlobal as xgg
from PySide2.QtWidgets import *


tex_template = "M:/BA/publish/assets/Character/{asset_name}/Shd/Shd/_tex"
publish_template = "M:/BA/publish/assets/Character/{asset_name}/Shd/Shd/_publish/maya/BA_{asset_name}_Shd_Shd.mb"
xgen_template = "M:/BA/publish/assets/Character/{asset_name}/Hair/Hair/_xgen/maya"


logger = logging.getLogger("Character")


class Path(object):
    def __init__(self, asset_name):
        self.asset_name = asset_name

    @property
    def tex_dir(self):
        return tex_template.format(asset_name=self.asset_name)

    @property
    def publish_path(self):
        return publish_template.format(asset_name=self.asset_name)

    @property
    def xgen_dir(self):
        return xgen_template.format(asset_name=self.asset_name)


class Xgen(object):

    def export_palette(self, palette, xgen_path):
        xgen_dir = os.path.dirname(xgen_path)
        if not os.path.isdir(xgen_dir):
            os.makedirs(xgen_dir)
        xgen.exportPalette(palette, xgen_path)

    def import_palette(self, xgen_path, deltas, namespace=None):
        if isinstance(deltas, basestring):
            deltas = [deltas]
        if not os.path.isfile(xgen_path):
            logger.warning("%s is not an exist path." % xgen_path)
            return
        xgen.importPalette(xgen_path, deltas, namespace)

    def create_delta(self, palette, delta_path):
        delta_dir = os.path.dirname(delta_path)
        if not os.path.isdir(delta_dir):
            os.makedirs(delta_dir)
        xgen.createDelta(palette, "D:/temp.xgd")
        shutil.copy("D:/temp.xgd", delta_path)
        os.remove("D:/temp.gxd")

    def set_abs_path(self, xgen_dir):
        if not xgg.Maya:
            return
        # palette is collection, use palettes to get collections first.
        palettes = xgen.palettes()
        for palette in palettes:
            # Use descriptions to get description of each collection
            descriptions = xgen.descriptions(palette)
            for description in descriptions:
                commaon_objs = xgen.objects(palette, description, True)
                fx_objs = xgen.fxModules(palette, description)
                objs = commaon_objs + fx_objs
                # Get active objs,e.g. SplinePrimtives
                for obj in objs:
                    attrs = xgen.allAttrs(palette, description, obj)
                    for attr in attrs:
                        value = xgen.getAttr(attr, palette, description, obj)
                        if "${DESC}" in value:
                            print palette, description, obj, attr
                            description_dir = os.path.join(xgen_dir, "collections", palette, description).replace("\\", "/")
                            new_value = value.replace("${DESC}", description_dir)
                            xgen.setAttr(attr, new_value, palette, description, obj)

        de = xgg.DescriptionEditor
        de.refresh("Full")


class Maya(object):
    def __init__(self, asset_name):
        self.asset_name = asset_name
        self.path = Path(self.asset_name)
        self.xg = Xgen()

    def copy_textures(self):
        file_nodes = mc.ls(type="file")
        if not file_nodes:
            return
        tex_dir = self.path.tex_dir
        if not os.path.isdir(tex_dir):
            os.makedirs(tex_dir)
        for file_node in file_nodes:
            texture = mc.getAttr("%s.fileTextureName" % file_node)
            if not os.path.isfile(texture):
                print "%s is not an exist file" % texture
                continue
            base_name = os.path.basename(texture)
            new_path = "%s/%s" % (tex_dir, base_name)
            if texture != new_path:
                shutil.copy(texture, new_path)
                mc.setAttr("%s.fileTextureName" % file_node, new_path, type="string")

    def copy_xgen_dir(self, old_xgen_dir):
        xgen_dir = self.path.xgen_dir
        if not os.path.isdir(xgen_dir):
            os.makedirs(xgen_dir)
        from distutils.dir_util import copy_tree
        copy_tree(old_xgen_dir, xgen_dir)
        return xgen_dir

    def set_xgen_path(self, old_xgen_dir):
        xgen_dir = self.copy_xgen_dir(old_xgen_dir)
        self.xg.set_abs_path(xgen_dir)

    def save_to_publish(self):
        publish_path = self.path.publish_path
        if not os.path.isdir(os.path.dirname(publish_path)):
            os.makedirs(os.path.dirname(publish_path))
        mc.file(rename=publish_path)
        mc.file(save=1, f=1, type="mayaBinary")


def run():
    # todo delete rig

    # ############
    asset_name, ok = QInputDialog.getText(None, "Input", "Asset Name")
    if not ok:
        return
    palettes = xgen.palettes()
    if palettes:
        xgen_dir = QFileDialog.getExistingDirectory()
        if not xgen_dir:
            return
    maya = Maya(asset_name)
    maya.copy_textures()
    logger.info("Copy textures done.")
    if palettes:
        maya.set_xgen_path(xgen_dir)
        logger.info("xgen done.")
    maya.save_to_publish()
    logger.info("Save to publish done.")
    QMessageBox(None, "Warming Tip", "Congratulations, All done.")


if __name__ == "__main__":
    run()
