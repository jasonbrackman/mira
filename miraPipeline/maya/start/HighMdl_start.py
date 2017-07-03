# -*- coding: utf-8 -*-
import optparse
import logging
import os
from miraLibs.mayaLibs import open_file, save_as, quit_maya
from miraLibs.pipeLibs import pipeFile


def main():
    logger = logging.getLogger("HighMdl start")
    # copy low mdl publish file as mdl file
    context = pipeFile.PathDetails.parse_path(options.file)
    project = context.project
    asset_type = context.asset_type
    asset_name = context.asset_name
    MidMdl_publish_file = pipeFile.get_asset_task_publish_file(project, asset_type, asset_name, "MidMdl", "MidMdl")
    logger.info("MidMdl publish file: %s" % MidMdl_publish_file)
    if not os.path.isfile(MidMdl_publish_file):
        logger.warning("No MidMdl file published.")
        quit_maya.quit_maya()
        return
    open_file.open_file(MidMdl_publish_file)
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
