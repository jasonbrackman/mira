# -*- coding: utf-8 -*-
import os
import imp
import optparse
import pipeGlobal
from miraLibs.pipeLibs import pipeFile


def publish(file_name, local=True):
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    step = context.step
    custom_dir = pipeGlobal.custom_dir
    publish_dir = os.path.join(custom_dir, project, "publish")
    if not os.path.isdir(publish_dir):
        publish_dir = os.path.join(custom_dir, "defaultProject", "publish")
    fn_, path, desc = imp.find_module(step, [publish_dir])
    mod = imp.load_module(step, fn_, path, desc)
    mod.main(file_name, local)


def main():
    file_name = options.file
    publish(file_name, local=False)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name"] if i in dir()]) == 1:
        options.file = file_name
        main()
