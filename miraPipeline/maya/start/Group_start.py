# -*- coding: utf-8 -*-
import optparse
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import save_as, quit_maya


def main():
    logger = logging.getLogger("Group start")
    # copy low mdl publish file as mdl file
    file_path = options.file
    context = pipeFile.PathDetails.parse_path(file_path)
    asset_name = context.asset_name
    asset_type_short_name = context.asset_type_short_name
    model_name = "%s_%s_MODEL" % (asset_type_short_name, asset_name)
    # create default group
    mc.group(name=model_name, empty=1)
    save_as.save_as(file_path)
    logger.info("%s publish successful!" % file_path)
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
