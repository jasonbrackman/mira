# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, "E:/miraSG")
from miraLibs.pipeLibs.get_task_name import get_task_name
import miraCore
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs import pipeMira, pipeFile, get_logger
from miraLibs.sgLibs import Sg
from miraLibs.pipeLibs.pipeSg import task_from_sg_path


class Publish(object):
    def __init__(self, work_file=None, change_task_status=True):
        self.work_file = work_file
        self.change_task_status = change_task_status
        self.obj = pipeFile.PathDetails.parse_path(self.work_file)
        self.logger = self.get_logger()
        self.engine = self.obj.engine
        self.project = self.obj.project

    def get_logger(self):
        task_name = get_task_name(self.obj)
        logger = get_logger.get_logger(self.obj.project, "publish", task_name)
        return logger

    def maya_publish(self):
        # publish mayabatch cmd to deadline
        script_dir = miraCore.get_scripts_dir()
        publish_dir = join_path.join_path2(script_dir, "pipeTools", self.engine, "publish")
        publish_py = join_path.join_path2(publish_dir, "%s_publish.py" % self.obj.step)
        if not os.path.isfile(publish_py):
            self.logger.error("%s is not an exist file" % publish_py)
            return
        mayabatch = pipeMira.get_mayabatch_path(self.obj.project)
        cmd = "%s -command \"python \\\"file_name='%s';execfile('%s')\\\"\"" % (
            mayabatch, self.work_file, publish_py)
        self.logger.info("cmd:\n\n%s\n\n" % cmd)
        return_file = os.popen(cmd)
        self.logger.info(return_file.read())
        return_file.close()
        self.post_publish()

    def nuke_publish(self):
        # todo
        pass

    def houdini_publish(self):
        # todo
        pass

    def post_publish(self):
        if not os.path.isfile(self.obj.publish_path):
            self.logger.error("Something wrong with publish")
            return
        # set task sg_publishfile
        self.logger.info("start post publish...")
        sg = Sg.Sg(self.project)
        current_task = task_from_sg_path.task_from_sg_path(sg, self.work_file)
        self.logger.info("Current Task: %s" % current_task)
        sg.update_task(current_task, sg_publishfile=self.obj.publish_path)
        self.logger.info("update task sg_publishfile: %s" % self.obj.publish_path)
        # change task status
        if self.change_task_status:
            sg.update_task_status(current_task, "cmpt")
            self.logger.info("update task sg_status_list: cmpt")
        self.logger.info("\n\nAll Done.")

    def main(self):
        if self.engine == "maya":
            self.maya_publish()
        elif self.engine == "nuke":
            self.nuke_publish()
        elif self.engine == "houdini":
            self.houdini_publish()


def main():
    work_file = sys.argv[1]
    change_task = sys.argv[2]
    p = Publish(work_file, change_task)
    p.main()


if __name__ == "__main__":
    main()



