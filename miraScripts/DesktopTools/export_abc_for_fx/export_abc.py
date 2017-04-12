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
import re
# Third-party modules

# Studio modules

# Local modules

logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_export_abc_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def export_abc():
    import maya.cmds as mc
    mc.file(options.file, open=1, pmt=1)
    print "[AAS] info: open file successful"

    # -----------------get export objects-------------------------- #
    objects = get_model_group()
    if not objects:
        print "[AAS] error: no MODEL group"
        mc.quit(f=1)
        return
    print "[AAS] info: model groups"
    print objects
    # -------------------fix frames-------------------------------- #
    mc.playbackOptions(e=1, min=options.start)
    mc.playbackOptions(e=1, max=options.end)
    # --------------------load plugin---------------------- ------- #
    if not mc.pluginInfo("AbcExport", q=1, loaded=1):
        try:
            mc.loadPlugin("AbcExport", quiet=1)
        except Exception as e:
            print "[AAS] error: %s" % e
            mc.quit(f=1)
            return
    # # ----------------- ------bake frames--------   ------------ #
    # from commonCore.core_mayaCommon import sk_sceneTools
    # reload(sk_sceneTools)
    # sk_sceneTools.sk_sceneTools().sk_sceneCameraUpdate(batchUpadate=1, bakeMode=1)
    # from commonCore.core_finalLayout import sk_cacheFinalLayout
    # reload(sk_cacheFinalLayout)
    # sk_cacheFinalLayout.sk_cacheFinalLayout().sk_checkBakeConstraints(step=1, fixEuler=0)
    camera_abc_dir = os.path.abspath(os.path.join(options.output, "cam"))
    if not os.path.isdir(camera_abc_dir):
        os.makedirs(camera_abc_dir)
    camera_path = os.path.abspath(os.path.join(camera_abc_dir, "camera.abc"))
    # ----------------------- get export camera-------------------- #
    valid_camera = get_valid_camera()
    j_base_string = "-frameRange {start_frame} {end_frame} -uvWrite -worldSpace" \
                        " -writeVisibility -file {tar_path}"
    if len(valid_camera) == 0:
        print "[AAS] warning: No valid camera"
    elif len(valid_camera) > 1:
        print "[AAS] warning: there's %s valid_camera %s " % (len(valid_camera), valid_camera)
    # -----------------------export baked camera------------------- #
    elif len(valid_camera) == 1:
        j_cam_string = j_base_string.format(tar_path=camera_path,
                                            start_frame=options.start,
                                            end_frame=options.end,)
        j_cam_string = "%s -root %s" % (j_cam_string, valid_camera[0])
        print "[AAS] info: start export camera"
        print "[AAS] info: %s" % j_cam_string
        try:
            mc.AbcExport(j=j_cam_string)
        except Exception as e:
            print "[AAS] error: %s" % e
            mc.quit(f=1)
            return
    # -----------------------export model abc------------------- #
    abc_file_dir = os.path.abspath(os.path.join(options.output, "asb"))
    if not os.path.isdir(abc_file_dir):
        os.makedirs(abc_file_dir)
    for root in objects:
        namespace = get_namespace_by_object(root)
        abc_file_name = os.path.abspath(os.path.join(abc_file_dir, namespace+".abc"))
        j_mdl_string = j_base_string.format(tar_path=abc_file_name,
                                            start_frame=options.start,
                                            end_frame=options.end)
        j_mdl_string += " -root %s" % root
        print "[AAS] info: start export %s" % root
        print "[AAS] info: %s" % j_mdl_string
        try:
            mc.AbcExport(j=j_mdl_string)
        except Exception as e:
            print "[AAS] error: %s" % e
    # -------------------------close maya----------------------- #
    mc.quit(f=1)


def get_valid_camera():
    cameras = mc.ls(type='camera')
    camera_pattern = r"^cam_\d+\w?_\d+\w?$"
    valid_camera = list()
    for camera in cameras:
        cam_trans = mc.listRelatives(camera, parent=True)[0]
        if re.match(camera_pattern, cam_trans):
            valid_camera.append(cam_trans)
    return valid_camera


def get_model_group():
    model_groups = list()
    for trans in mc.ls(type='transform'):
        if trans.endswith(":MODEL"):
            model_groups.append(trans)
    return model_groups


def get_namespace_by_object(object_name):
    namespace = mc.referenceQuery(object_name, namespace=1)
    namespace = namespace.strip(":")
    namespace = namespace.replace(":", "__")
    return namespace


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="Maya file ma or mb", metavar="string")
    parser.add_option("-s", dest="start", help="start frame", metavar="int")
    parser.add_option("-e", dest="end", help="end frame", metavar="int")
    parser.add_option("-o", dest="output", help="output dir", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    parser.add_option("-l", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -l\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["abc_file", "abc_start", "abc_end", "abc_output"] if i in dir()]) == 4:
        options.file = abc_file
        options.start = abc_start
        options.end = abc_end
        options.output = abc_output
        export_abc()
