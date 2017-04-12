#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_export_abc
# description : ''
# author      : HeShuai
# date        : 2016/1/13
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import optparse
import subprocess
# Third-party modules

# Studio modules

# Local modules



logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_export_abc_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def run_command(command):
    print "[AAS] info: Running command \"%s\"" % command
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        return_code = p.poll()
        if return_code == 0:
            break
        elif return_code == 1:
            raise Exception(command + "was terminated for some reason.")
        elif return_code is not None:
            print "[AAS] error: exit return code is: %s" % str(return_code)
            raise Exception(command + "was crashed for some reason.")
        line = p.stdout.readline()
        if line.strip():
            print line


def export_abc():
    import maya.cmds as mc
    mc.file(options.file, open=1, pmt=1)
    print "[AAS] info: open file successful"
    # get export objects
    objects = mc.ls('*:MODEL')
    # if not objects:
    #     print "[AAS] error: no MODEL group"
    #     return
    # fix frames
    mc.playbackOptions(e=1, min=options.start)
    mc.playbackOptions(e=1, max=options.end)
    # load plugin
    if not mc.pluginInfo("AbcExport", q=1, loaded=1):
        mc.loadPlugin("AbcExport", quiet=1)
    # create abc folder
    abc_folder = os.path.dirname(options.output)
    print options.output
    if not os.path.isdir(abc_folder):
        os.makedirs(abc_folder)
    # get export camera
    cameras = mc.ls(cameras=True)
    cam_trans = [mc.listRelatives(camera, parent=True)[0] for camera in cameras]
    print cam_trans


def do_export_abc():
    import add_environ
    from utility.py_utils import get_path_utility

    this = __file__.replace("\\", "/")
    options.file = options.file.replace("\\", "/")
    mayabatch = get_path_utility.get_maya_batch(options.file)

    command = "\"%s\" -command \"python \\\"abc_file='%s';" \
              "abc_start=%s;abc_end=%s;abc_output='%s';execfile('%s')\\\"\"" % \
              (mayabatch, options.file, options.start, options.end, options.output, this)
    run_command(command)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="Maya file ma or mb", metavar="string")
    parser.add_option("-s", dest="start", help="start frame", metavar="int")
    parser.add_option("-e", dest="end", help="end frame", metavar="int")
    parser.add_option("-o", dest="output", help="output path", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if all((options.file, options.start, options.end, options.output)):
        do_export_abc()
    elif len([i for i in ["abc_file", "abc_start", "abc_end", "abc_output"] if i in dir()]) == 4:
        options.file = abc_file
        options.start = abc_start
        options.end = abc_end
        options.output = abc_output
        export_abc()
