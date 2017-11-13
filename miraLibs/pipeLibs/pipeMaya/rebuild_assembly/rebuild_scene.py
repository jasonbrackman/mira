import logging
import os
import maya.cmds as mc
import maya.mel as mel
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import conf_parser
from miraLibs.mayaLibs import Assembly, create_group


def get_anim_edit_data():
    context = pipeFile.PathDetails.parse_path()
    if context.step == "LgtLay":
        description_path = pipeFile.get_task_file(context.project, context.sequence, context.shot,
                                                  "AnimLay", "AnimLay", "maya_shot_description", "")
    elif context.step == "Lgt":
        description_path = pipeFile.get_task_file(context.project, context.sequence, context.shot,
                                                  "Anim", "Anim", "maya_shot_description", "")
    if os.path.isfile(description_path):
        cp = conf_parser.ConfParser(description_path)
        conf_data = cp.parse().get()
        return conf_data
    else:
        print "%s is not an exist file." % description_path


def edit(conf_data=None):
    if not conf_data:
        conf_data = get_anim_edit_data()
    if not conf_data:
        return
    edits = conf_data.get("edits")
    if not edits:
        print "No edits found."
        return
    for e in edits:
        try:
            mel.eval(e)
        except:
            print "Error: %s" % e
    print "Edit done."


def rebuild_scene():
    # get logger
    logger = logging.getLogger(__name__)
    # get conf data
    anim_edit_data = get_anim_edit_data()
    name = anim_edit_data.get("owner")
    def_path = anim_edit_data.get("definition")
    # create AR node
    assemb = Assembly.Assembly()
    ar_node = assemb.reference_ad(name, def_path)
    logger.info("Create %s done." % ar_node)
    # edit
    edit(anim_edit_data)
    logger.info("anim edit done.")
    # set parent
    create_group.create_group("Env")
    mc.parent(ar_node, "Env")
    logger.info("Set parent done.")
