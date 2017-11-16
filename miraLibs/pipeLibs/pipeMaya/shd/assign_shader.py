# -*- coding: utf-8 -*-
import re
import os
import logging
from Qt.QtWidgets import *
import maya.cmds as mc
import miraLibs.pipeLibs.pipeFile as pipeFile
from miraLibs.pyLibs import json_operation
from miraLibs.mayaLibs import create_reference, get_namespace
from miraLibs.mayaLibs import get_maya_globals


ASSET_DICT = {"char": "Character", "prop": "Prop", "cprop": "Cprop", "env": "Environment", "build": "Building"}
logger = logging.getLogger(__name__)
not_exist_geo_list = []
not_exist_sg_list = []


def get_project():
    maya_globals = get_maya_globals.get_maya_globals()
    project = maya_globals.get("currentProject").project
    return project


def exist_warning(value):
    logger.warning("Maya Node does not exist: %s" % value)


def set_renderer_attribute(json_data, mesh, final_mesh):
    attrs = ["rsEnableSubdivision", "rsSubdivisionRule", "rsScreenSpaceAdaptive", "rsDoSmoothSubdivision",
             "rsMinTessellationLength", "rsMaxTessellationSubdivs", "rsOutOfFrustumTessellationFactor",
             "rsEnableDisplacement", "rsMaxDisplacement", "rsDisplacementScale", "rsAutoBumpMap"]
    for attr in attrs:
        try:
            attr_value = json_data.get(mesh).get(attr)
            if attr_value is not None:
                mc.setAttr("%s.%s" % (final_mesh, attr), json_data.get(mesh).get(attr))
        except:
            pass


def assign_shader_to_another(json_data, mesh, final_mesh):
    sg_node = json_data.get(mesh).get("sg")
    is_mesh_exist = mc.objExists(final_mesh)
    is_sg_exist = mc.objExists(sg_node)
    if not is_mesh_exist:
        exist_warning(mesh)
        not_exist_geo_list.append(mesh)
        return
    if not is_sg_exist:
        exist_warning(sg_node)
        not_exist_sg_list.append(sg_node)
        return
    try:
        mc.sets(final_mesh, fe=sg_node)
    except:
        logger.error("Can not assign shader: %s ---> mesh: %s" % (sg_node, final_mesh))
    set_renderer_attribute(json_data, mesh, mesh)


class Asset(object):
    def __init__(self, name=None):
        self.name = name
        self.long_name = mc.ls(self.name, long=1)[0]
        self.project = get_project()

    @property
    def asset_type_short_name(self):
        return self.name.split(":")[-1].split("_")[0]

    @property
    def asset_type(self):
        return ASSET_DICT.get(self.asset_type_short_name)

    @property
    def asset_name(self):
        return self.name.split(":")[-1].split("_")[1]

    @property
    def prefix(self):
        prefix = "|".join((self.long_name.split("|")[:-1]))
        return prefix

    @property
    def namespace(self):
        namespace_name = get_namespace.get_namespace(self.name)
        namespace_name = namespace_name.strip(":")
        return namespace_name

    @property
    def suffix(self):
        pattern = ".*MODEL(\d+)$"
        matched = re.match(pattern, self.name)
        if matched:
            return matched.group(1)

    @property
    def json_path(self):
        json_path = pipeFile.get_task_file(self.project, self.asset_type, self.asset_name,
                                           "Shd", "Shd", "maya_asset_connection", "")
        return json_path

    @property
    def json_data(self):
        json_path = self.json_path
        if json_path and os.path.isfile(json_path):
            json_data = json_operation.get_json_data(json_path)
            return json_data
        else:
            logger.warning("%s is not an exist file" % json_path)

    @property
    def shd_path(self):
        shd_path = pipeFile.get_task_file(self.project, self.asset_type, self.asset_name,
                                          "Shd", "Shd", "maya_asset_shd", "")
        if shd_path and os.path.isfile(shd_path):
            return shd_path
        else:
            logger.warning("%s is not an exist file" % shd_path)


def reference_shd(shd_path):
    shd_path = shd_path.replace("\\", "/")
    reference_files = mc.file(q=1, r=1, wcn=1)
    if shd_path in reference_files:
        return  
    create_reference.create_reference(shd_path)


def assign_shader(model_group_name):
    """
    assign shader by json configuration
    :param model_group_name: MODEL group
    :return:
    """
    asset = Asset(model_group_name)
    # below split(":") maybe some reference with namespace
    json_data = asset.json_data
    if not json_data:
        return
    # get shd path and reference in
    shd_path = asset.shd_path
    if not shd_path:
        return
    # assign shader
    prefix = asset.prefix
    suffix = asset.suffix
    namespace_name = asset.namespace
    # create reference
    reference_shd(shd_path)
    # has no parent group
    for mesh in json_data:
        mesh_list = mesh.split("|")
        if not prefix:
            if not suffix:
                if not namespace_name:
                    final_mesh = mesh
                else:
                    final_mesh = ("|%s:" % namespace_name).join(mesh_list)
            else:
                if not namespace_name:
                    mesh_list[1] = asset.name
                    final_mesh = "|".join(mesh_list)
                else:
                    tmp_mesh = ("|%s:" % namespace_name).join(mesh_list)
                    tmp_mesh_list = tmp_mesh.split("|")
                    tmp_mesh_list[1] = asset.name
                    final_mesh = "|".join(tmp_mesh_list)
        # has prefix (has parent group)
        else:
            if not suffix:
                if not namespace_name:
                    final_mesh = prefix + mesh
                else:
                    final_mesh = ("|%s:" % namespace_name).join(mesh_list)
                    final_mesh = prefix + final_mesh
            else:
                if not namespace_name:
                    mesh_list[1] = asset.name
                    final_mesh = "%s%s" % (prefix, "|".join(mesh_list))
                else:
                    tmp_mesh = ("|%s:" % namespace_name).join(mesh_list)
                    tmp_mesh_list = tmp_mesh.split("|")
                    tmp_mesh_list[1] = asset.name
                    final_mesh = "%s%s" % (prefix, "|".join(tmp_mesh_list))
        assign_shader_to_another(json_data, mesh, final_mesh)
    print "#" * 100
    print "Not exist transform:\n", "\t\n".join(not_exist_geo_list)
    print "#" * 100
    print "Not exist shadingEngine:\n", "\t\n".join(not_exist_sg_list)
    print "#" * 100


def main():
    asset = mc.ls(sl=1)
    if len(asset) == 1 and re.match(".*MODEL(\d+)?$", asset[0]):
        assign_shader(asset[0])
        QMessageBox.information(None, "Warming Tip", "Assign shader done.")
    else:
        logger.error("Select right group.")
        QMessageBox.critical(None, "Warming Tip", "Select right group please.")


if __name__ == "__main__":
    main()
