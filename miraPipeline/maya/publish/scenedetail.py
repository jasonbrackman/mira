# -*- coding: utf-8 -*-
import os
import optparse
import logging
import time
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.backup import backup
from miraLibs.mayaLibs import open_file, quit_maya, save_as, remove_reference_by_group, load_plugin, new_file
from miraLibs.pyLibs import create_parent_dir, copy


def main():
    logger = logging.getLogger("scenedetail publish")
    new_file.new_file()
    load_plugin.load_plugin("mtoa.mll")
    load_plugin.load_plugin("AbcImport.mll")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    obj = pipeFile.PathDetails.parse_path(file_path)
    publish_path = obj.publish_path
    # export gpu cache
    '''
    gpu_cache_path = pipeFile.get_shot_step_gpucache_file(seq, shot, "sceneset", project)
    create_parent_dir.create_parent_dir(gpu_cache_path)
    gpu_directory = os.path.dirname(gpu_cache_path)
    gpu_file_name = os.path.splitext(os.path.basename(gpu_cache_path))[0]
    logger.info("Exporting gpu cache...")
    export_gpu_cache.export_gpu_cache("sceneset", gpu_directory, gpu_file_name, 1, 1)
    logger.info("Export gpu cache to %s" % gpu_cache_path)
    backup.backup(project, gpu_cache_path, False)
    '''
    # replace workarea v000
    workarea_file_path = file_path.replace("_QCPublish", "_workarea")
    # backup.backup(project, workarea_file_path, False)
    copy.copy(file_path, workarea_file_path)
    logger.info("Cover %s" % workarea_file_path)
    # remove camera reference
    remove_reference_by_group.remove_reference_by_group("camera")
    remove_reference_by_group.remove_reference_by_group("_TEMP")
    logger.info("remove camera and remove _TEMP")
    # save to publish path
    create_parent_dir.create_parent_dir(publish_path)
    save_as.save_as(publish_path)
    logger.info("Save to %s" % publish_path)
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
