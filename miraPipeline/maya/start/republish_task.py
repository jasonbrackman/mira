# -*- coding: utf-8 -*-
import os
import logging
import optparse
from miraLibs.pipeLibs.pipeMaya.network import change_network
from miraLibs.mayaLibs import open_file, save_as, quit_maya
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import get_new_version


def republish_task():
    logger = logging.getLogger(__name__)
    obj = pipeFile.PathDetails.parse_path(options.file)
    project = obj.project
    open_file.open_file(options.file)
    change_network.change_network(project=project, task_id=options.task_id)
    logger.info("change TaskId: %s" % options.task_id)
    next_version_file = get_new_version.get_new_version(options.file)[0]
    save_as.save_as(next_version_file)
    quit_maya.quit_maya()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-t", dest="task_id", help="maya file ma or mb.", metavar="int")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name", "task_id"] if i in dir()]) == 2:
        options.file = file_name
        options.task_id = task_id
        republish_task()
