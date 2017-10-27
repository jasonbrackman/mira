# -*- coding: utf-8 -*-
import os
import logging
import time
from miraLibs.pipeLibs import Project
from miraLibs.pyLibs import join_path


def get_logger(project, logger_type, task_name):
    logger_dir = Project(project).task_log_dir
    logger_dir = logger_dir.format(project=project)
    logger_dir = join_path.join_path2(logger_dir, logger_type)
    if not os.path.isdir(logger_dir):
        os.makedirs(logger_dir)
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    file_base_name = "%s-%s.txt" % (task_name, current_time)
    file_name = join_path.join_path2(logger_dir, file_base_name)
    logging.basicConfig(filename=file_name,
                        level=logging.DEBUG, filemode='w', format='%(asctime)s - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    return logger
