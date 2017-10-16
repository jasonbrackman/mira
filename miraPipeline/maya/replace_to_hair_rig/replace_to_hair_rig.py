# -*- coding: utf-8 -*-
import os
import logging
from Qt.QtWidgets import *
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import replace_reference


def replace_to_hair_rig():
    selected = mc.ls(sl=1)
    if len(selected) > 1:
        logging.error("Please specify a single node or file name.")
        return
    is_reference = mc.referenceQuery(selected, isNodeReferenced=1)
    if not is_reference:
        logging.error("Please specify a reference node.")
        return
    message_box = QMessageBox.information(None, "Warming Tip", "Make sure replace to HairRig",
                                          QMessageBox.Yes | QMessageBox.Cancel)
    if message_box.name == "Cancel":
        return
    ref_node = mc.referenceQuery(selected, referenceNode=1)
    ref_file = mc.referenceQuery(selected, filename=1, wcn=1)
    context = pipeFile.PathDetails.parse_path(ref_file)
    if context.step in ["MidRig", "HighRig"]:
        hair_rig_file = pipeFile.get_task_file(context.project, context.asset_type,
                                               context.asset_name, "HairRig", "HairRig", "maya_asset_publish", "")
        if os.path.isfile(hair_rig_file):
            replace_reference.replace_reference(ref_node, hair_rig_file)
        else:
            logging.warning("No hair rig file exist.")


if __name__ == "__main__":
    replace_to_hair_rig()
