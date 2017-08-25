import logging
import maya.cmds as mc
import maya.app.general.editUtils as editUtils
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import conf_parser


def get_owner():
    context = pipeFile.PathDetails.parse_path()
    sequence = context.sequence
    owner = "%s_c000_set" % sequence
    if mc.objExists(owner):
        return owner


def get_all_edits(owner):
    all_edits = list()
    ar_nodes = mc.ls(type="assemblyReference")
    for ar_node in ar_nodes:
        edits = editUtils.getEdits(owner, ar_node)
        if not edits:
            continue
        edits = [str(i.getString()) for i in edits]
        all_edits.extend(edits)
    return all_edits


def export_scene():
    logger = logging.getLogger(__name__)
    # get description path
    context = pipeFile.PathDetails.parse_path()
    yml_path = context.definition_path
    # get owner
    owner = get_owner()
    if not owner:
        logger.error("%s does not exist" % owner)
        return
    # get owner definition path
    definition_path = str(mc.getAttr("%s.def" % owner))
    # get all edits
    all_edits = get_all_edits(owner)
    # write out to description path
    info_dict = dict(owner=owner, definition=definition_path, edits=all_edits)
    cp = conf_parser.ConfParser(yml_path)
    cp.parse().set(info_dict)
