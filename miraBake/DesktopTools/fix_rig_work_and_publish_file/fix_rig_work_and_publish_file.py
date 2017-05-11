#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_fix_rig_work_and_publish_file
# description : ''
# author      : HeShuai
# date        : 2016/1/26
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import subprocess
# Third-party modules

# Studio modules

# Local modules
import add_environ
import aas_libs.aas_sg as aas_sg
import aas_libs.aas_util as aas_util
from utility.py_utils import get_path_utility


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_fix_rig_work_and_publish_file_log.txt'),
                    level=logging.DEBUG, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


class FixRig(object):
    def __init__(self):
        self.sg_utils = aas_sg.SgUtility()
        self.tk = aas_sg.get_tk_object()

    def get_need_fix_files(self):
        all_tasks = self.sg_utils.get_all_asset_rig_tasks("DF", "Character")
        all_maya_files = list()
        for task in all_tasks:
            # publish path
            try:
                publish_path = aas_sg.get_task_path(self.tk, "tk-maya", task, "maya_asset_publish")
                latest_publish_path = aas_util.get_latest_version(publish_path)
                if not latest_publish_path:
                    print "[AAS] info: %s has no publish file" % task["content"]
                    logging.info("[AAS] info: %s has no publish file" % task["content"])
                else:
                    all_maya_files.append(latest_publish_path[0])
            except Exception as e:
                print "[AAS] error: %s" % e
                logging.error(str(e))
            # work path
            try:
                work_path = aas_sg.get_task_path(self.tk, "tk-maya", task, "maya_asset_work")
                latest_work_path = aas_util.get_latest_version(work_path)
                if not latest_work_path:
                    print "[AAS] info: %s has no publish file" % task["content"]
                    logging.info("[AAS] info: %s has no work file" % task["content"])
                else:
                    all_maya_files.append(latest_work_path[0])
            except Exception as e:
                print "[AAS] error: %s" % e
                logging.error(str(e))
        return all_maya_files

    def get_fix_fig_path(self):
        current_path = __file__
        fix_rig_path = os.path.abspath(os.path.join(os.path.dirname(current_path), "fix_rig.py"))
        fix_rig_path = fix_rig_path.replace("\\", "/")
        return fix_rig_path

    def get_command_list(self):
        fix_rig_path = self.get_fix_fig_path()
        maya_files = self.get_need_fix_files()
        mayabatch = "C:/tools/Autodesk/Maya2014/bin/mayabatch.exe"
        command_list = list()
        for maya_file in maya_files:
            maya_file = maya_file.replace("\\", "/")
            command = "\"%s\" -command \"python \\\"rig_file='%s';" \
                      "execfile('%s')\\\"\"" % \
                      (mayabatch, maya_file, fix_rig_path)
            command_list.append(command)
        return command_list

    def main(self):
        command_list = self.get_command_list()
        num = len(command_list)
        for command in command_list:
            print command
            print "*"*50
            print "%s left" % num
            print "*"*50
            logging.info(command)
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while True:
                return_code = p.poll()
                if return_code == 0:
                    break
                elif return_code == 1:
                    command_info = "[AAS] error: %s was terminated for some reason." % command
                    logging.error(command_info)
                    raise Exception(command_info)
                elif return_code is not None:
                    command_info = "[AAS] error: exit return code is: %s" % str(return_code)
                    logging.error(command_info)
                    raise Exception(command_info)
                line = p.stdout.readline()
                if line.strip():
                    print line
            print "[AAS] info %s has finished" % command
            logging.info("%s has finished" % command)
            num -= 1
        print "[AAS] info: All tasks are finished"
        logging.info("All tasks are finished")


if __name__ == "__main__":
    fr = FixRig()
    fr.main()
