# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc


class Maya(object):
    def __init__(self, asset_dir):
        self.asset_dir = asset_dir
        self.mdl_path = self.get_mdl_path()
        self.shd_path = self.get_shd_path()

    def launch_folder(self):
        from asset_library_libs.start_file import start_file
        start_file(self.asset_dir)

    def get_mdl_path(self):
        name = os.path.basename(self.asset_dir)
        mdl_path = os.path.join(self.asset_dir, "_mdl", "%s.abc" % name)
        mdl_path = mdl_path.replace("\\", "/")
        return mdl_path

    def get_shd_path(self):
        name = os.path.basename(self.asset_dir)
        shd_path = os.path.join(self.asset_dir, "_shd", "%s.mb" % name)
        if not os.path.isfile(shd_path):
            shd_path = os.path.join(self.asset_dir, "_shd", "%s.ma" % name)
        shd_path = shd_path.replace("\\", "/")
        return shd_path

    @staticmethod
    def get_file_type(path):
        if path.endswith(".mb"):
            file_type = "mayaBinary"
        elif path.endswith(".ma"):
            file_type = "mayaAscii"
        elif path.endswith(".abc"):
            file_type = "Alembic"
        return file_type

    def maya_import(self, path):
        if not os.path.isfile(path):
            logging.error("%s is not an exist file." % path)
            return
        file_type = self.get_file_type(path)
        mc.file(path, i=1, ignoreVersion=1, ra=1, mergeNamespacesOnClash=0,
                namespace=":", pr=1, typ=file_type)

    def maya_reference(self, path):
        if not os.path.isfile(path):
            logging.error("%s is not an exist file." % path)
            return
        file_type = self.get_file_type(path)
        base_name = os.path.basename(path)
        name = os.path.splitext(base_name)[0]
        mc.file(path, r=1, ignoreVersion=1, gl=1, mergeNamespacesOnClash=0,
                namespace=name, typ=file_type)

    def maya_import_mdl(self):
        self.maya_import(self.mdl_path)

    def maya_import_shd(self):
        self.maya_import(self.shd_path)

    def maya_reference_mdl(self):
        self.maya_reference(self.mdl_path)

    def maya_reference_shd(self):
        self.maya_reference(self.shd_path)
