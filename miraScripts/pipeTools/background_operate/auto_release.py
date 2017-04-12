# -*- coding: utf-8 -*-
import sys,datetime
sys.path.insert(0, "Z:/mira")
from miraScripts.pipeTools.task_release import release_proc


def auto_release():
    project_name = sys.argv[1]
    taskId = sys.argv[2]
    log_path = sys.argv[3]
    nowTime = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
    task_dict = {'taskId': taskId, 'taskEndDate': nowTime}
    release_proc.releaseFunction(task_dict,project_name,log_path)


if __name__ == '__main__':
    auto_release()
