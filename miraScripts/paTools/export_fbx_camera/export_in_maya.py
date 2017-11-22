# -*- coding: utf-8 -*-
import os
import optparse
import maya.cmds as mc
from miraLibs.mayaLibs import import_abc, bake_frame, quit_maya


def get_wanted_camera():
    wanted_camera = None
    objects = mc.ls(assemblies=1)
    for obj in objects:
        if obj.startswith("cam"):
            wanted_camera = obj
            break
    return wanted_camera


def main():
    # import camera abc
    abc_file = options.file
    abc_dir = os.path.dirname(abc_file)
    start = options.start
    end = options.end
    import_abc.import_abc(abc_file)
    # bak frames
    camera = get_wanted_camera()
    bake_frame.bake_frame(camera, start, end)
    # export fbx
    fbx_file = "%s/%s.fbx" % (abc_dir, camera)
    mc.select(camera)
    mc.file(fbx_file, options="", typ="FBX export", force=1, pr=1, es=1)
    os.startfile(abc_dir)
    quit_maya.quit_maya()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name", "start", "end"] if i in dir()]) == 3:
        options.file = file_name
        options.start = start
        options.end = end
        main()
