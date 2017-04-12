# -*- coding: utf-8 -*-
import os
import optparse
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import quit_maya, new_file, create_reference, load_plugin, create_group
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya.rebuild_scene import rebuild_scene


def main():
    logger = logging.getLogger("sceneset start")
    file_name = options.file
    obj = pipeFile.PathDetails.parse_path(file_name)
    project = obj.project
    seq = obj.seq
    shot = obj.shot
    # new file
    new_file.new_file()
    # save as options.file
    mc.file(rename=file_name)
    create_group.create_group("scenelight")
    # rebuild sceneset
    # -get yml path from layout
    logger.info("Rebuild scene start...")
    yml_path = pipeFile.get_shot_step_connection_file(seq, shot, "lay", project)
    if not os.path.isfile(yml_path):
        raise EOFError("%s is not an exist file" % yml_path)
    rebuild_scene.rebuild_scene(yml_path)
    logger.info("Rebuild scene done.")
    # -reference in _TEMP
    tempgeo_path = pipeFile.get_shot_step_tempgeo_file(seq, shot, "lay", project)
    if not os.path.isfile(tempgeo_path):
        raise EOFError("%s is not an exist file" % tempgeo_path)
    # load plugin AbcImport.mll
    load_plugin.load_plugin("AbcImport.mll")
    mc.file(tempgeo_path, r=1, namespace=":", ignoreVersion=1, type="Alembic", gl=1, mergeNamespacesOnClash=False)
    try:
        mc.parent("_TEMP", "sceneset")
    except:
        pass
    logger.info("Reference _TEMP done.")
    # -reference in camera
    camera_path = pipeFile.get_shot_step_camera_file(seq, shot, "lay", project)
    if not os.path.isfile(camera_path):
        raise EOFError("%s is not an exist file" % camera_path)
    create_reference.create_reference(camera_path)
    logger.info("Reference camera done.")
    mc.file(save=1, f=1)
    logger.info("%s publish successful!" % file_name)
    quit_maya.quit_maya()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name"] if i in dir()]) == 1:
        options.file = file_name
        main()