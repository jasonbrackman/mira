# -*- coding: utf-8 -*-
import os
import optparse
import logging
from miraLibs.mayaLibs import new_file, save_as, quit_maya, create_reference, create_group
from miraLibs.pipeLibs import pipeFile


def main():
    logger = logging.getLogger("scenelight start")
    new_file.new_file()
    obj = pipeFile.PathDetails.parse_path(options.file)
    project = obj.project
    seq = obj.seq
    shot = obj.shot
    # reference in scenedetail publish file
    scenedetail_publish_file = pipeFile.get_shot_step_publish_file(seq, shot, "scenedetail", project)
    if not os.path.isfile(scenedetail_publish_file):
        raise RuntimeError("%s is not an exist file." % scenedetail_publish_file)
    create_reference.create_reference(scenedetail_publish_file)
    # create lights group
    create_group.create_group("lights")
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
