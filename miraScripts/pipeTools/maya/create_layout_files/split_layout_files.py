# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from PySide import QtGui, QtCore
from miraLibs.mayaLibs import select_current_view_objects


def clear_panel():
    mc.modelEditor('modelPanel4', e=1, allObjects=0)
    mc.modelEditor('modelPanel4', e=1, lights=1)
    mc.modelEditor('modelPanel4', e=1, pm=1)


def get_object_of_shot(shot):
    start_frame = int(mc.getAttr("%s.startFrame" % shot))
    end_frame = int(mc.getAttr("%s.endFrame" % shot))
    camera = mc.listConnections("%s.currentCamera" % shot)[0]
    if not camera:
        return
    mc.lookThru(camera)
    selected_objects = list()
    for frame in xrange(start_frame, end_frame+1):
        select_current_view_objects.select_current_view_objects()
        frame_selected_objects = mc.ls(sl=1, r=1)
        selected_objects.extend(frame_selected_objects)
    if selected_objects:
        selected_objects.append(camera)
        selected_objects = list(set(selected_objects))
        return selected_objects


def get_work_path(shot):
    project_name = shot.split('_', 1)[0]
    sequence_name = shot.split('_', 1)[1].split('_')[0]
    shot_name = shot.split('_', 1)[1].split('_')[1]
    root_lay_work_path = "D:/test/sequence"
    lay_task_work_dir = os.path.abspath(os.path.join(root_lay_work_path, project_name, sequence_name, shot_name, "lay"))
    lay_file_base_name = "%s_%s_%s_lay_v001.mb" % (project_name, sequence_name, shot_name)
    lay_task_work_path = os.path.abspath(os.path.join(lay_task_work_dir, lay_file_base_name))
    return lay_task_work_path


def main():
    clear_panel()
    shots = mc.ls(type="shot")
    progress_dialog = QtGui.QProgressDialog('Exporting...Please Wait', 'Cancel', 0, len(shots))
    progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
    progress_dialog.show()
    value = 0
    for shot in shots[:2]:
        progress_dialog.setValue(value)
        if progress_dialog.wasCanceled():
            break
        mc.select(clear=1)
        shot_objects = get_object_of_shot(shot)
        if not shot_objects:
            continue
        shot_lay_work_path = get_work_path(shot)
        mc.select(shot_objects, r=1)
        mc.file(shot_lay_work_path, force=1, options="v=0", type="mayaBinary", preserveReferences=1, exportSelected=1)
        value += 1


if __name__ == "__main__":
    main()
