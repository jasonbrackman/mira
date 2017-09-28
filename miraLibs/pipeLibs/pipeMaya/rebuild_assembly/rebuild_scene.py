import logging
import maya.cmds as mc
import maya.mel as mel
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import conf_parser
from miraLibs.mayaLibs import Assembly, create_group


def get_conf_data():
    context = pipeFile.PathDetails.parse_path()
    description_path = pipeFile.get_task_file(context.project, context.sequence, context.shot,
                                              "AnimLay", "AnimLay", "maya_shot_description", "")
    cp = conf_parser.ConfParser(description_path)
    conf_data = cp.parse().get()
    return conf_data


def edit(conf_data=None):
    if not conf_data:
        conf_data = get_conf_data()
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
    conf_data = get_conf_data()
    name = conf_data.get("owner")
    def_path = conf_data.get("definition")
    # create AR node
    assemb = Assembly.Assembly()
    ar_node = assemb.reference_ad(name, def_path)
    logger.info("Create %s done." % ar_node)
    # edit
    edit(conf_data)
    logger.info("Edit done.")
    # set parent
    create_group.create_group("Env")
    mc.parent(ar_node, "Env")
    logger.info("Set parent done.")
