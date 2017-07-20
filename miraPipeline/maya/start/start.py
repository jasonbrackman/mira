# -*- coding: utf-8 -*-
import os
import sys
import imp
import optparse
import miraCore
from miraLibs.pipeLibs import pipeFile


def main():
    file_name = options.file
    context = pipeFile.PathDetails.parse_path(file_name)
    step = context.step
    engine = context.engine
    pipeline_dir = miraCore.get_pipeline_dir()
    start_dir = os.path.join(pipeline_dir, engine, "start")
    fn_, path, desc = imp.find_module(step, [start_dir])
    mod = imp.load_module(step, fn_, path, desc)
    mod.main(file_name)


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
