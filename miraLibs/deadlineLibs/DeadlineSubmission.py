# -*- coding: utf-8 -*-
import subprocess
import time
import os
import re
import logging
from miraLibs.pyLibs.Temporary import Temporary
from miraLibs.pipeLibs import pipeMira, pipeFile
from miraLibs.pyLibs import copy


class DeadlineSubmission(object):
    def __init__(self):
        object.__init__(self)
        self.jobid = None

        self.executable = pipeMira.get_executable().get("py27").get("pythonbin")
        self.arguments = '-c "import time; time.sleep(10)"'
        self.cwd = pipeMira.get_executable().get("py27").get('pythonstartupdir')

        self.details = {"Plugin": "CommandLine",
                        "Name": "",
                        "Comment": '',
                        "Department": 'Automated',
                        "SecondaryPool": '',
                        "Group": "all",
                        "Priority": "70",
                        "TaskTimeoutMinutes": "0",
                        "EnableAutoTimeout": "False",
                        "ConcurrentTasks": "1",
                        "LimitConcurrentTasksToNumberOfCpus": "True",
                        "MachineLimit": "0",
                        "Whitelist": '',
                        "LimitGroups": '',
                        "JobDependencies": "",
                        "OnJobComplete": "Nothing",
                        "Frames": "0",
                        "ChunkSize": "1",
                        "ExtraInfo0": ""
                        }
        pool = pipeMira.get_executable().get("deadline").get("default_pool")
        if pool:
            self.setPool(pool)

    def setCWD(self, cwd):
        self.cwd = cwd

    def setExe(self, exe):
        self.executable = exe

    def setArgs(self, args):
        self.arguments = args

    def setName(self, name):
        self.details['Name'] = name

    def setPool(self, pool):
        self.details['Pool'] = pool

    def setFrames(self, frames):
        self.details['Frames'] = str(frames)

    def setChunkSize(self, size):
        self.details['ChunkSize'] = str(size)

    def setJobDependencies(self, dep):
        self.details['JobDependencies'] = dep

    def submit(self):
        with Temporary() as tempdir:
            job_info, plugin_info = self.settingjobPlugininfo(tempdir)
            command = "%s %s %s" % (pipeMira.get_executable().get("deadline").get("path"), job_info, plugin_info)
            logging.info("submitting command %s", command)

            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False)
            p.wait()

            jobid_match = re.compile("JobID=(?P<jobid>[a-z0-9]{24})")
            for x in p.stdout:
                match = jobid_match.match(x)
                if match:
                    self.jobid = match.groupdict()["jobid"]
                    break
        return self.jobid

    def settingjobPlugininfo(self, tempdir):
        jobSubmission = {
            'Arguments': self.arguments,
            'Executable': self.executable,
            'StartupDirectory': self.cwd,
        }
        job_info = os.path.join(tempdir, "jobinfo.job")
        DeadlineSubmission.write_keys(self.details, job_info)
        plugin_info = os.path.join(tempdir, "info.publin")
        DeadlineSubmission.write_keys(jobSubmission, plugin_info)
        return job_info, plugin_info

    @staticmethod
    def write_keys(keypairs, keyfile):
        string = ''
        for key in keypairs:
            string += '%s=%s\n' % (key, keypairs[key])
        with open(keyfile, 'w') as f:
            f.write(string)
        return keyfile

    def waitUntilComplete(self):
        condition = True
        while condition:
            progress = self.get_job_progress()
            if progress == 100:
                return
            time.sleep(1)

    def get_job_progress(self):
        cmd = pipeMira.get_executable().get("deadline").get("path") + " GetTaskProgress " + self.jobid
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        p.wait()
        progress_match = re.compile("JobProgress=(?P<progress>[0-9]+)%")
        for x in p.stdout:
            match = progress_match.match(x)
            if match:
                return int(match.groupdict()["progress"])


def submit_maya():
    import sys
    import pymel.core as pm
    # this will submit a job to deadline with the current maya scene's settings. It's just a placeholder at the moment
    # until we get our GUI up and running with this style of command line submission.
    context = pipeFile.PathDetails.parse_path()
    filein = context.work_path
    if not os.path.isfile(filein):
        copy.copy(pm.sceneName(), filein)
    maya.mel.eval('setMayaSoftwareFrameExt(3,0);')
    # dets = pft.PathDetails.parse_path(pm.sceneName())
    # fileout = dets.getRenderFullPath().split('.####.')[0]
    # pm.setAttr('defaultRenderGlobals.imageFilePrefix', fileout)
    maya_dir = os.path.dirname(sys.executable)
    maya_exex = '%s\Render.exe' % maya_dir
    startframe = int(pm.playbackOptions(animationStartTime=True, query=True))
    endframe = int(pm.playbackOptions(animationEndTime=True, query=True))
    name = os.path.split(filein)[1]
    # comment = ''

    maya_args = '-s <STARTFRAME>  -e <ENDFRAME>  %s' % filein

    sub = DeadlineSubmission()
    sub.setExe(maya_exex)
    sub.setArgs(maya_args)
    sub.setName(name)
    sub.setFrames("%s-%s" % (startframe, endframe))
    sub.setChunkSize(1)
    sub.submit()
