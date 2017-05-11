# -*- coding: utf-8 -*-
import optparse
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import save_as, create_group, quit_maya
from miraLibs.pipeLibs import pipeFile
# from miraLibs.pipeLibs.pipeMaya.rebuild_scene import rebuild_scene


def main():
    logger = logging.getLogger("layout start")
    obj = pipeFile.PathDetails.parse_path(options.file)
    project = obj.project
    seq = obj.seq
    shot = obj.shot
    # create camera and create group
    camera_name = "cam_%s_%s" % (seq, shot)
    create_group.create_group("camera")
    cam = mc.camera()
    mc.rename(cam[1], "%sShape" % camera_name)
    camera = mc.rename(cam[0], camera_name)
    mc.parent(camera, "camera")
    # mc.lockNode(camera, l=1)
    create_group.create_group("env")
    create_group.create_group("char")
    create_group.create_group("prop")
    create_group.create_group("_REF")
    create_group.create_group("render")
    # set frame range
    mc.playbackOptions(e=1, minTime=101)
    mc.playbackOptions(e=1, maxTime=150)
    # # rebuild scene
    # logger.info("rebuild scene start...")
    # result = rebuild_scene.rebuild_scene(options.file)
    # if not result:
    #     raise RuntimeError("Something wrong with rebuild scene.")
    # logger.info("rebuild scene done.")
    # save as start file
    save_as.save_as(options.file)

    save_as.save_as(options.file)
    logger.info("%s publish successful!" % options.file)
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