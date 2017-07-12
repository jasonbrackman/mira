# -*- coding: utf-8 -*-
import optparse
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish


def main():
    logger = logging.getLogger("MidRig publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_path)
    # copy image
    publish.copy_image_and_video(context)
    logger.info("Copy image and video done.")
    # import all reference
    publish.reference_opt()
    logger.info("Import reference done.")
    # export needed
    publish.export_need_to_publish(context, "rig")
    logger.info("Export to publish path done.")
    # add to AD
    publish.add_mesh_to_ad(context)
    logger.info("Add to AD done.")
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
