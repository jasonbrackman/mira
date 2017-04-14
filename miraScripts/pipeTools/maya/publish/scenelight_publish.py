# -*- coding: utf-8 -*-
import logging
import time
import optparse
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.backup import backup
from miraLibs.pipeLibs.pipeMaya.network import delete_network
from miraLibs.mayaLibs import open_file, quit_maya, save_as
from miraLibs.pyLibs import create_parent_dir, copy
from miraLibs.pipeLibs.pipeDb import sql_api


def main():
    logger = logging.getLogger("sceneset publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    obj = pipeFile.PathDetails.parse_path(file_path)
    project = obj.project
    publish_path = obj.publish_path
    workarea_file_path = file_path.replace("_QCPublish", "_workarea")
    # backup.backup(project, workarea_file_path, False)
    copy.copy(file_path, workarea_file_path)
    logger.info("Cover %s" % workarea_file_path)
    # add to database
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    task_id = int(mc.getAttr("ROOT.task_id"))
    db = sql_api.SqlApi(project)
    arg_dict = {'taskId': task_id, 'taskEndDate': current_time}
    db.releaseTask(arg_dict)
    logger.info("Add to data base.")
    # save to publish path
    delete_network.delete_network()
    create_parent_dir.create_parent_dir(publish_path)
    save_as.save_as(publish_path)
    logger.info("Save to %s" % publish_path)
    backup.backup(project, publish_path, False)
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
