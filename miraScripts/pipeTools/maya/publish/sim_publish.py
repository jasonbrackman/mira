# -*- coding: utf-8 -*-
import optparse
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import publish_to_db
from miraLibs.mayaLibs import delete_all_lights, quit_maya, save_as
from miraLibs.mayaLibs import open_file
from miraLibs.pipeLibs.pipeMaya.network import delete_network


def main():
    logger = logging.getLogger("sim publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get path
    obj = pipeFile.PathDetails.parse_path(file_path)
    project = obj.project
    publish_path = obj.publish_path
    # add to database
    publish_to_db.publish_to_db(project)
    logger.info("Add to data base.")
    # save to publish path
    delete_all_lights.delete_all_lights()
    delete_network.delete_network()
    save_as.save_as(publish_path)
    logger.info("save to publish path: %s" % publish_path)
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
