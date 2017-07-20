# -*- coding: utf-8 -*-
import optparse
import logging
from miraLibs.mayaLibs import new_file, save_as, create_group, quit_maya
from miraLibs.pipeLibs import pipeFile


def main():
    logger = logging.getLogger("sceneset start")
    new_file.new_file()
    create_group.create_group("env")
    save_as.save_as(options.file)
    # create network node
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
