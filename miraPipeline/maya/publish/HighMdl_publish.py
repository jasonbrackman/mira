# -*- coding: utf-8 -*-
import logging
import os
import optparse
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import get_model_name
from miraLibs.mayaLibs import export_gpu_cache, open_file, quit_maya, \
    export_selected, delete_layer, hierarchy_opt, import_gpu_cache, new_file, save_as
from miraLibs.pyLibs import create_parent_dir


def main():
    logger = logging.getLogger("mdl publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    obj = pipeFile.PathDetails.parse_path(file_path)
    publish_path = obj.publish_path
    asset_type = obj.asset_type
    model_name = get_model_name.get_model_name()
    # export _MODEL group to publish path
    delete_layer.delete_layer()
    mc.select(model_name, r=1)
    export_selected.export_selected(publish_path)
    # export gpu cache
    if asset_type in ["Prop"]:
        # export gpu cache
        gpu_cache_path = obj.gpu_cache_path
        create_parent_dir.create_parent_dir(gpu_cache_path)
        gpu_directory = os.path.dirname(gpu_cache_path)
        gpu_file_name = os.path.splitext(os.path.basename(gpu_cache_path))[0]
        logger.info("Exporting gpu cache...")
        export_gpu_cache.export_gpu_cache(model_name, gpu_directory, gpu_file_name, 1, 1)
        logger.info("Export gpu cache to %s" % gpu_cache_path)
        # generate a gpu mb file
        gpu_wrap_path = obj.gpuwrap_path
        new_file.new_file()
        gpu_shape_name = "%s_%s_GPUShape" % (obj.asset_type_short_name, obj.asset_name)
        gpu_name = "%s_%s_GPU" % (obj.asset_type_short_name, obj.asset_name)
        import_gpu_cache.import_gpu_cache(gpu_shape_name, gpu_name, gpu_cache_path)
        save_as.save_as(gpu_wrap_path)
    if asset_type in ["Character", "Prop"]:
        # write out topology
        topology_path = obj.topology_path
        model_name = get_model_name.get_model_name()
        ho = hierarchy_opt.HierarchyOpt(model_name)
        ho.write_out(topology_path)
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
