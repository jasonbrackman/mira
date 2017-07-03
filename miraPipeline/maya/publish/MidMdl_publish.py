# -*- coding: utf-8 -*-
import os
import logging
import optparse
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish


logger = logging.getLogger("MidMdl publish")


def main():
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    context = pipeFile.PathDetails.parse_path()
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    publish.export_need_to_publish(context)
    logger.info("export to publish done.")
    publish.export_model_to_abc(context)
    logger.info("export to abc done")
    publish.create_ad(context)
    logger.info("create ad done")
    # quit maya
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
