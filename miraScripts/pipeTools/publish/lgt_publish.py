# -*- coding: utf-8 -*-
import logging
import optparse
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import save_as, open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya.network import delete_network


def main():
    logger = logging.getLogger("lgt publish")
    file_path = options.file
    open_file.open_file(file_path)
    obj = pipeFile.PathDetails.parse_path(file_path)
    publish_path = obj.publish_path
    # save to publish path
    delete_network.delete_network()
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
