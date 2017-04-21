# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, "Z:/miraSG")
from miraLibs.pipeLibs.get_task_name import get_task_name
import miraCore
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs import pipeMira, pipeFile, get_logger
from miraLibs.sgLibs import Sg
from miraLibs.pipeLibs.pipeSg import task_from_sg_path, create_filesystem_structure


class Start(object):
    def __init__(self, work_file):
        self.work_file = work_file
        self.obj = pipeFile.PathDetails.parse_path(self.work_file)
        self.project = self.obj.project
        self.engine = self.obj.engine
        self.logger = self.get_logger()

    def get_logger(self):
        task_name = get_task_name(self.obj)
        logger = get_logger.get_logger(self.project, "create", task_name)
        return logger

    def maya_start(self):
        script_dir = miraCore.get_scripts_dir()
        start_dir = join_path.join_path2(script_dir, "pipeTools", self.engine, "start")
        start_py = join_path.join_path2(start_dir, "%s_start.py" % self.obj.step)
        if not os.path.isfile(start_py):
            self.logger.error("%s is not an exist file" % start_py)
            return
        mayabatch = pipeMira.get_mayabatch_path(self.project)
        cmd = "%s -command \"python \\\"file_name='%s';execfile('%s')\\\"\"" % (
            mayabatch, self.work_file, start_py)
        self.logger.info("cmd:\n\n%s\n\n" % cmd)
        return_file = os.popen(cmd)
        self.logger.info(return_file.read())
        return_file.close()
        self.post_start()

    def nuke_start(self):
        # todo
        pass

    def houdini_start(self):
        # todo
        pass

    def post_start(self):
        if not os.path.isfile(self.work_file):
            self.logger.error("Something wrong with start")
            return
        # set task sg_startfile
        self.logger.info("start post start...")
        sg = Sg.Sg(self.project)
        current_task = task_from_sg_path.task_from_sg_path(sg, self.work_file)
        create_filesystem_structure.create_filesystem_structure(self.work_file, engine="tk-%s" % self.engine)
        self.logger.info("Current Task: %s" % current_task)
        # update sg_workfile
        sg.update_task(current_task, sg_workfile=self.work_file)
        self.logger.info("update task sg_workfile: %s" % self.work_file)
        # update sg_status_list
        sg.update_task_status(current_task, "rdy")
        self.logger.info("update task sg_status_list: rdy")
        self.logger.info("\n\nALL Done!")

    def main(self):
        if self.engine == "maya":
            self.maya_start()
        elif self.engine == "nuke":
            self.nuke_start()
        elif self.engine == "houdini":
            self.houdini_start()


def main():
    work_file = sys.argv[1]
    p = Start(work_file)
    p.main()


if __name__ == "__main__":
    main()
