# -*- coding: utf-8 -*-
from miraScripts.pipeTools.task_release.release_UI import release_UI
import datetime, sys
sys.path.insert(0,'Z:/mira')


def deadline_release():
    taskId = sys.argv[1]
    nowTime = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
    taskDict = {'taskId': taskId, 'taskEndDate': nowTime}
    release_UI('sct').releaseFunction(taskDict)

if __name__ =='__main__':
    deadline_release()