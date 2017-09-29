# -*- coding: utf-8 -*-
import os
import logging
import xgenm as xgen
import xgenm.xgGlobal as xgg
from miraLibs.pyLibs import copy
import xgenm.XgExternalAPI as xge


logger = logging.getLogger("Xgen")


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
        copy.copy("D:/temp.xgd", delta_path)
        os.remove("D:/temp.xgd")
        
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

