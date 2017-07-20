# -*- coding: utf-8 -*-
import os
import sys
import imp
import optparse
from miraLibs.pipeLibs import pipeFile


def get_start_dir():
    start_dir = os.path.dirname(sys.argv[0])
    return start_dir


def main():
    file_name = options.file
    context = pipeFile.PathDetails.parse_path(file_name)
    step = context.step
    start_dir = get_start_dir()
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
