# -*- coding: utf-8 -*-
import logging
import optparse
import maya.cmds as mc
from miraLibs.mayaLibs import import_load_remove_unload_ref, open_file, save_as, \
    quit_maya, export_selected, delete_layer
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya.network import delete_network
from miraLibs.pipeLibs.pipeMaya import publish_to_db


def main():
    logger = logging.getLogger("hair publish")
    file_path = options.file
    open_file.open_file(file_path)
    obj = pipeFile.PathDetails.parse_path(file_path)
    asset_type_short_name = obj.asset_type_short_name
    asset_name = obj.asset_name
    project = obj.project
    publish_path = obj.publish_path
    hair_path = obj.hair_path
    yeti_group = "%s_%s_yetiNode" % (asset_type_short_name, asset_name)
    # import mdl reference
    import_load_remove_unload_ref.import_load_remove_unload_ref()
    # export yeti group to _hair group
    delete_layer.delete_layer()
    mc.select(yeti_group, r=1)
    export_selected.export_selected(hair_path)
    logger.info("export yeti node to _hair done.")
    mc.delete(yeti_group)
    # add to database
    publish_to_db.publish_to_db(project)
    logger.info("Add to data base.")
    # save to publish path
    delete_network.delete_network()
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
