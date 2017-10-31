# -*- coding: utf-8 -*-
import subprocess
import time
import os
import re
import logging
from miraLibs.pyLibs.Temporary import Temporary
import pipeGlobal


class DeadlineSubmission(object):
    def __init__(self):
        object.__init__(self)
        self.jobid = None

        self.executable = pipeGlobal.exe.get("python").get("py27").get("pythonbin")
        self.arguments = '-c "import time; time.sleep(10)"'
        self.cwd = pipeGlobal.exe.get("python").get("py27").get('pythonstartupdir')

        self.details = {"Plugin": "CommandLine",
                        "Name": "",
                        "Comment": '',
                        "Department": 'Automated',
                        "SecondaryPool": '',
                        "Group": "",
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
                        "ExtraInfo0": "",
                        "UserName": ""
                        }
        pool = pipeGlobal.exe.get("deadline").get("default_pool")
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

    def setUserName(self, name):
        self.details["UserName"] = name

    def submit(self):
        with Temporary() as tempdir:
            job_info, plugin_info = self.settingjobPlugininfo(tempdir)
            command = '"%s" "%s" "%s"' % (pipeGlobal.exe.get("deadline").get("path"), job_info, plugin_info)
            logging.info("submitting command %s", command)
            # in maya
            p = subprocess.Popen(command)
            p.wait()
        #   # in python
        #     p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False)
        #     p.wait()
        #
        #     jobid_match = re.compile("JobID=(?P<jobid>[a-z0-9]{24})")
        #     for x in p.stdout:
        #         match = jobid_match.match(x)
        #         if match:
        #             self.jobid = match.groupdict()["jobid"]
        #             break
        # return self.jobid

    def settingjobPlugininfo(self, tempdir):
        jobSubmission = {
            'Arguments': self.arguments,
            'Executable': self.executable,
            'StartupDirectory': self.cwd
        }
        job_info = os.path.join(tempdir, "jobinfo.job").replace("\\", "/")
        DeadlineSubmission.write_keys(self.details, job_info)
        plugin_info = os.path.join(tempdir, "info.publin").replace("\\", "/")
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
        cmd = pipeGlobal.exe.get("deadline").get("path") + " GetTaskProgress " + self.jobid
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        p.wait()
        progress_match = re.compile("JobProgress=(?P<progress>[0-9]+)%")
        for x in p.stdout:
            match = progress_match.match(x)
            if match:
                return int(match.groupdict()["progress"])

