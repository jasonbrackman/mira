# -*- coding: utf-8 -*-
import os
import sys
import logging
sys.path.insert(0, "E:/mira")
import optparse
import subprocess
try:
    import maya.cmds as mc
except:pass
try:
    import miraLibs.mayaLibs.offset_anim_keyframe as offset_anim_keyframe
    from miraLibs.mayaLibs import select_current_view_objects
except:pass


def clear_panel():
    mc.modelEditor('modelPanel4', e=1, allObjects=0)
    mc.modelEditor('modelPanel4', e=1, lights=1)
    mc.modelEditor('modelPanel4', e=1, pm=1)


def get_object_of_shot(shot):
    # start_frame = int(mc.getAttr("%s.startFrame" % shot))
    # end_frame = int(mc.getAttr("%s.endFrame" % shot))
    camera = mc.listConnections("%s.currentCamera" % shot)[0]
    # if not camera:
    #     return
    # # mc.lookThru(camera)
    # selected_objects = list()
    # for frame in xrange(start_frame, end_frame+1):
    #     select_current_view_objects.select_current_view_objects()
    #     frame_selected_objects = mc.ls(sl=1, r=1)
    #     selected_objects.extend(frame_selected_objects)
    # if selected_objects:
    #     selected_objects.append(camera)
    #     selected_objects = list(set(selected_objects))
    return ["TrainingPlace_df_TrainingPlace_mdl:MODEL", camera]


def get_work_path(shot):
    project_name = shot.split('_', 1)[0]
    sequence_name = shot.split('_', 1)[1].split('_')[0]
    shot_name = shot.split('_', 1)[1].split('_')[1]
    root_lay_work_path = "D:/test/sequence"
    lay_task_work_dir = os.path.abspath(os.path.join(root_lay_work_path, project_name, sequence_name, shot_name, "lay"))
    lay_file_base_name = "%s_%s_%s_lay_v001.mb" % (project_name, sequence_name, shot_name)
    lay_task_work_path = os.path.abspath(os.path.join(lay_task_work_dir, lay_file_base_name))
    return lay_task_work_path


def split_layout_files():
    print options.file
    mc.file(options.file, open=1, pmt=1, f=1)
    clear_panel()
    shots = mc.ls(type="shot")
    all_shot_lay_work_path = list()
    for shot in shots:
        mc.select(clear=1)
        shot_objects = get_object_of_shot(shot)
        if not shot_objects:
            continue
        shot_lay_work_path = get_work_path(shot)
        all_shot_lay_work_path.append(shot_lay_work_path)
        mc.select(shot_objects, r=1)
        mc.file(shot_lay_work_path, force=1, options="v=0", type="mayaBinary", preserveReferences=1, exportSelected=1)
    return all_shot_lay_work_path


def offset_keyframe(to_frame=1001):
    mc.file(options.file, open=1, pmt=1, f=1)
    # get offset
    shot = mc.ls(type="shot")
    if not len(shot) == 1:
        logging.error("Not one shot in the maya file")
        return
    start_frame = mc.getAttr("%s.sequenceStartFrame" % shot[0])
    end_frame = mc.getAttr("%s.sequenceEndFrame" % shot[0])
    frame_num = end_frame-start_frame+1
    frame_offset_value = to_frame-start_frame
    # offset all keyframes
    all_curves = mc.ls(type="animCurve")
    valid_curves = list()
    for curve in all_curves:
        is_ref = mc.referenceQuery(curve, inr=1)
        if not is_ref:
            valid_curves.append(curve)
    offset_anim_keyframe.offset_anim_keyframe(valid_curves, frame_offset_value)
    mc.playbackOptions(e=1, min=to_frame)
    mc.playbackOptions(e=1, max=to_frame+frame_num)
    # delete shot
    mc.delete(shot)
    mc.file(save=1, f=1)


def run_command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        return_code = p.poll()
        if return_code == 0:
            break
        elif return_code == 1:
            raise Exception('maya was terminated for some reason')
        elif return_code != None:
            print 'exit return code is:'+str(return_code)
            raise Exception('maya was crashed for some reason.')
        line = p.stdout.readline()
        if line.strip():
            print line


def split_layout_files_bg():
    maya_batch = "C:/tools/Autodesk/Maya2014/bin/mayabatch.exe"
    log_path = "D:/test/pv.log"
    cmd = "%s -log \"%s\" -command \"python(\\\"pv_file='%s';execfile('%s')\\\")\"" % \
          (maya_batch, log_path, options.file, __file__.replace("\\", "/"))
    print "@@@@", cmd
    run_command(cmd)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="Maya file ma or mb", metavar="string")
    parser.add_option("-t", dest="type", help="pv or layout", metavar="string")
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
    if options.file:
        split_layout_files_bg()
    if len([i for i in ["pv_file"] if i in dir()]) == 1:
        options.file = pv_file
        layout_files = split_layout_files()
        for layout_file in layout_files:
            options.file = layout_file
            offset_keyframe()
        try:
            mc.quit(f=1)
        except:pass
