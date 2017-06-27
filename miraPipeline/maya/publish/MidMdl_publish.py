# -*- coding: utf-8 -*-
import logging
import optparse
import maya.cmds as mc
from miraLibs.pyLibs import copy
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import get_model_name
from miraLibs.mayaLibs import open_file, quit_maya, export_selected, delete_layer, export_abc


def main():
    logger = logging.getLogger("MidMdl publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    obj = pipeFile.PathDetails.parse_path(file_path)
    image_path = obj.image_path
    video_path = obj.video_path
    publish_path = obj.publish_path
    abc_cache_path = obj.abc_cache_path
    final_path = obj.final_path
    final_image_path = obj.final_image_path
    final_video_path = obj.final_video_path
    final_cache_path = obj.final_cache_path
    model_name = get_model_name.get_model_name()
    # export _MODEL group to publish path
    delete_layer.delete_layer()
    mc.select(model_name, r=1)
    export_selected.export_selected(publish_path)
    # export abc
    if obj.asset_type in ["Prop", "Character"]:
        logger.info("Exporting abc...")
        export_abc.export_abc(1, 1, abc_cache_path, model_name, False)
        logger.info("Exporting abc done")
    # copy to final
    copy.copy(image_path, final_image_path)
    copy.copy(video_path, final_video_path)
    copy.copy(publish_path, final_path)
    copy.copy(abc_cache_path, final_cache_path)
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
