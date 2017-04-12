# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import re
import threading


def get_run_app():
    app = sys.executable
    app_basename = os.path.basename(app)
    app_name = os.path.splitext(app_basename)[0]
    return app_name


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
        self.maya_path_dict = {"2016": "C:/tools/Autodesk/Maya2016/bin/maya.exe"}

    def get_may_version(self):
        ext = os.path.splitext(self.path)[1].lower()
        f = open(self.path, "r")
        line = f.readline()
        if ext == ".ma":
            r = re.findall(r'//Maya ASCII (\d+) scene', line, re.I)
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
        maya_version = self.get_may_version()
        if not maya_version:
            return
        maya_path = self.maya_path_dict[str(maya_version)]
        cmd = "%s %s" % (maya_path, self.path)
        thread = RunCommandThread(cmd)
        thread.start()
        self.threads.append(thread)

    def run(self):
        app = get_run_app()
        if app == "maya":
            self.run_in_maya()
        elif app == "python":
            self.run_standalone()


class FileOpener(object):
    def __init__(self, path):
        self.path = path.replace("\\", "/")
        self.ext = os.path.splitext(self.path)[-1]

    def run(self):
        if self.ext in [".ma", ".mb"]:
            opener = MayaOpener(self.path)
        else:
            opener = None
        if opener:
            opener.run()


if __name__ == "__main__":
    fo = FileOpener(r"Z:\mnt\shotgun\projects\snowkid\assets\Character\Snowman\lowMdl\lowMdl\_workarea\maya\snowkid_Snowman_lowMdl_v000.mb")
    fo.run()
