# -*- coding: utf-8 -*-
import optparse
import os
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, save_as


def main():
    logger = logging.getLogger("anim start")
    obj = pipeFile.PathDetails.parse_path(options.file)
    project = obj.project
    seq = obj.seq
    shot = obj.shot
    # find layout publish file
    lay_publish_file = pipeFile.get_shot_step_publish_file(seq, shot, "lay", project)
    if not os.path.isfile(lay_publish_file):
        raise RuntimeError("%s is not an exist file." % lay_publish_file)
    # add frame range attribute
    open_file.open_file(lay_publish_file)
    start_frame = int(mc.playbackOptions(q=1, min=1))
    end_frame = int(mc.playbackOptions(q=1, max=1))
    cam_name = "cam_%s_%s" % (seq, shot)
    mc.lockNode(cam_name, l=0)
    mc.addAttr(cam_name, ln="frame_range", dataType="string")
    mc.setAttr("%s.frame_range" % cam_name, e=1, keyable=1)
    mc.setAttr("%s.frame_range" % cam_name, "%s-%s" % (start_frame, end_frame), type="string")
    mc.setAttr("%s.frame_range" % cam_name, l=1)

    save_as.save_as(options.file)
    logger.info("%s publish successful!" % options.file)
    quit_maya.quit_maya()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-t", dest="task_id", help="maya file ma or mb.", metavar="int")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name", "task_id"] if i in dir()]) == 2:
        options.file = file_name
        options.task_id = task_id
        main()
