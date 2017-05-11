# -*- coding: utf-8 -*-
import optparse
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, delete_layer
from miraLibs.pipeLibs.pipeMaya import get_model_name, rename_pipeline_shape
from miraLibs.mayaLibs import export_selected, import_load_remove_unload_ref


def main():
    logger = logging.getLogger("rig publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    obj = pipeFile.PathDetails.parse_path(file_path)
    publish_path = obj.publish_path
    # import all reference
    import_load_remove_unload_ref.import_load_remove_unload_ref()
    logger.info("Import all reference.")
    # rename shape
    if not rename_pipeline_shape.rename_pipeline_shape():
        raise RuntimeError("Rename shape error.")
    # export rig root group
    delete_layer.delete_layer()
    rig_group = get_model_name.get_model_name(context="rig")
    mc.select(rig_group, r=1)
    export_selected.export_selected(publish_path)
    logger.info("Export %s to %s" % (rig_group, publish_path))
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
