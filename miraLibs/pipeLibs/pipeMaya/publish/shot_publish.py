# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import new_file, Assembly, save_file

logger = logging.getLogger("miraLibs.pipeLibs.pipeMaya.asset_publish")


def create_shot_ad(context):
    ad_path = context.definition_path
    if os.path.isfile(ad_path):
            return
    ad_node_name = "%s_%s_AD" % (context.sequence, context.shot)
    if not os.path.isfile(context.publish_path):
        logger.error("%s is not an exist file" % context.publish_path)
        return
    new_file.new_file()
    mc.file(rename=ad_path)
    assemb = Assembly.Assembly()
    node = assemb.create_assembly_node(ad_node_name, "assemblyDefinition")
    assemb.create_representation(node, "MayaScene", "env", "env", context.publish_path)
    save_file.save_file()
