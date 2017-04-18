# -*- coding: utf-8 -*-
import os
import logging
import optparse
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, export_gpu_cache, delete_all_lights, save_as
from miraLibs.pyLibs import create_parent_dir
from miraLibs.pipeLibs.pipeMaya.rebuild_scene import export_scene


def main():
    logger = logging.getLogger("sceneset publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    obj = pipeFile.PathDetails.parse_path(file_path)
    project = obj.project
    connection_path = obj.connection_path
    gpu_cache_path = obj.gpu_cache_path
    publish_path = obj.publish_path
    # export gpu cache
    create_parent_dir.create_parent_dir(gpu_cache_path)
    gpu_directory = os.path.dirname(gpu_cache_path)
    gpu_file_name = os.path.splitext(os.path.basename(gpu_cache_path))[0]
    logger.info("Exporting gpu cache...")
    export_gpu_cache.export_gpu_cache("env", gpu_directory, gpu_file_name, 1, 1)
    logger.info("Export gpu cache to %s" % gpu_cache_path)
    # build a scene description
    export_scene.export_scene(connection_path)
    # delete all lights
    delete_all_lights.delete_all_lights()
    save_as.save_as(publish_path)
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
