# -*- coding: utf-8 -*-
import subprocess
import os
import re
import threading
from get_engine import get_engine
import pipeGlobal


class RunCommandThread(threading.Thread):

    def __init__(self, command=None):
        super(RunCommandThread, self).__init__()
        self.__command = command

    def run(self):
        p = subprocess.Popen(self.__command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            return_code = p.poll()
            if return_code == 0:
                break
            elif return_code == 1:
                raise Exception(self.__command + " was terminated for some reason.")
            elif return_code is not None:
                raise Exception(self.__command + " was crashed for some reason.")
            line = p.stdout.readline()
            if line.strip():
                print line


class MayaOpener(object):
    def __init__(self, path):
        self.path = path
        self.threads = list()

    def get_maya_version(self):
        ext = os.path.splitext(self.path)[1].lower()
        with open(self.path, "r") as f:
            line = f.readline()
            if ext == ".ma":
                r = re.findall(r'//Maya ASCII (\d+).* scene', line, re.I)
                if r:
                    return int(r[0])
            else:
                r = re.findall(r'.*\rversion\x00(\d+).*', line, re.I)
                if r:
                    return int(r[0])

    def run_in_maya(self):
        import maya.cmds as mc
        mc.file(self.path, open=1, f=1)

    def run_standalone(self):
        maya_version = self.get_maya_version()
        if not maya_version:
            return
        maya_path = pipeGlobal.exe.get("maya").get(maya_version).get("path")
        cmd = "%s %s" % (maya_path, self.path)
        thread = RunCommandThread(cmd)
        thread.start()
        self.threads.append(thread)

    def run(self):
        app = get_engine()
        if app == "maya":
            self.run_in_maya()
        else:
            self.run_standalone()


class NukeOpener(object):
    def __init__(self, path):
        self.path = path
        self.threads = list()

    def get_nuke_version(self):
        with open(self.path, "r") as f:
            lines = f.readlines()
            for line in lines:
                matched = re.match("^version (.*)", line)
                if matched:
                    nuke_version = matched.group(1)
                    return nuke_version

    def run_in_nuke(self):
        import nuke
        nuke.scriptClose(ignoreUnsavedChanges=True)
        nuke.scriptOpen(self.path)

    def run_standalone(self):
        nuke_version = self.get_nuke_version()
        if not nuke_version:
            return
        nuke_path = pipeGlobal.exe.get("nuke").get(nuke_version).get("path")
        cmd = "%s %s" % (nuke_path, self.path)
        thread = RunCommandThread(cmd)
        thread.start()
        self.threads.append(thread)

    def run(self):
        app = get_engine()
        if app == "nuke":
            self.run_in_nuke()
        else:
            self.run_standalone()


class FileOpener(object):
    def __init__(self, path):
        self.path = path.replace("\\", "/")
        self.ext = os.path.splitext(self.path)[-1]

    def run(self):
        if not os.path.isfile(self.path):
            print "FileOpener: %s is not an exist file." % self.path
            return
        opener = None
        if self.ext in [".ma", ".mb"]:
            opener = MayaOpener(self.path)
        elif self.ext in [".nk"]:
            opener = NukeOpener(self.path)
        if opener:
            opener.run()


if __name__ == "__main__":
    fo = FileOpener(r"Z:\mnt\shotgun\projects\snowkid\assets\Character\Snowman\lowMdl\lowMdl\_workarea\maya\snowkid_Snowman_lowMdl_v000.mb")
    fo.run()
