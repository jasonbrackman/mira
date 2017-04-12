# -*- coding: utf-8 -*-
import os
import logging
import copy
import maya.cmds as mc
from get_hud_object import get_hud_object
import miraLibs.pyLibs.avi_to_mov as avi_to_mov
from miraLibs.mayaLibs import display_smooth_shaded


def playblaster(file_name, camera=None, start_frame=None, end_frame=None, width_height=(2048, 858), percent=100,
                useTraxSounds=True, sound=None, open_it=True, use_sequence_time=False):
    display_smooth_shaded.display_smooth_shaded()
    ext = os.path.splitext(file_name)[-1]
    if ext == ".avi":
        movie_format = "avi"
        compression = "none"
    elif ext == ".mov":
        movie_format = "qt"
        compression = "PNG"
    else:
        logging.error(
            "Value Error: unsupported format.(must be an '.avi' or '.mov' file.)")
        raise Exception("Value Error: unsupported format.(must be an '.avi' or '.mov' file.)")
    # get frame range
    if not start_frame:
        start_frame = mc.playbackOptions(q=1, minTime=1)
    if not end_frame:
        end_frame = mc.playbackOptions(q=1, maxTime=1)
    # -get sound
    if useTraxSounds:
        sound = None
    # playblast sequence
    if use_sequence_time:
        camera = None
    parms = {
        "filename": file_name,
        "startTime": start_frame,
        "endTime": end_frame,
        "sound": sound,
        "useTraxSounds": useTraxSounds,
        "percent": percent,
        "format": movie_format,
        "compression": compression,
        "quality": 70,
        "viewer": open_it,
        "widthHeight": width_height,
        "showOrnaments": 1,
        "clearCache": 1,
        "framePadding": 4,
        "forceOverwrite": True,
        "offScreen": False,
        "sequenceTime": use_sequence_time
    }
    # -show huds
    hud_obj = get_hud_object()
    hud_obj.camera = camera
    hud_obj.show()
    # execute playblast
    do_playblast(parms, camera, open_it)
    # clear hub
    hud_obj.clear()


def do_playblast(parms, camera, open_it=True):
    # get final camera
    # -confirm camera
    avi_parms = copy.deepcopy(parms)
    if parms["format"] == "avi":
        avi_parms["filename"] = os.path.splitext(avi_parms["filename"])[0] + ".avi"
        avi_parms["format"] = "avi"
        avi_parms["compression"] = "none"
    if camera:
        if not mc.objExists(camera):
            mc.confirmDialog(
                title="Warning", message="{0} not found, make sure camera {0} exist".format(camera), button="OK")
            return
        # # -set camera attrs
        set_camera_settings(camera)
    else:
        cameras = get_cameras()
        if not cameras:
            return
        for camera in cameras:
            set_camera_settings(camera)
    # --do playblast
    logging.info(avi_parms)
    display_mode()
    try:
        mc.playblast(**avi_parms)
    except:
        logging.error("playblast failed.")
    # finally:
    #     if camera:
    #         mc.evalDeferred('import maya.cmds as mc;\nmc.deleteUI("%s", pnl=True)' % playblast_panel)
    # convert
    if parms["format"] == "avi":
        avi_to_mov.avi_to_mov(avi_parms["filename"], remove_src=True, openit=open_it)
    if camera:
        mc.setAttr("%s.overscan" % camera, 1)
    else:
        cameras = get_cameras()
        if cameras:
            for camera in cameras:
                mc.setAttr("%s.overscan" % camera, 1)
    return True


def display_mode():
    display_keys = ['nc', 'pl', 'lt', 'ca', 'joints', 'ikh', 'df', 'ha', 'follicles',
                    'hairSystems', 'strokes', 'motionTrails', 'dimensions', 'locators']
    # Display smoothness low
    model_panels = mc.getPanel(typ="modelPanel")
    for currentPanel in model_panels:
        for item in display_keys:
            eval("mc.modelEditor(\'"+currentPanel+"\',e=True,"+item+"=0)")


def set_camera_settings(camera):
    mc.setAttr("%s.displayGateMaskColor" % camera, 0, 0, 0, type="double3")
    mc.setAttr("%s.overscan" % camera, 1)
    attr_list_0 = ["dfc", "dfg", "dfo", "dfp", "dst", "displaySafeAction"]
    attr_list_1 = ["displayResolution", "displayGateMaskOpacity"]
    for attr in attr_list_0:
        mc.setAttr("{cam}.{attr}".format(cam=camera, attr=attr), 0)
    for attr in attr_list_1:
        mc.setAttr("{cam}.{attr}".format(cam=camera, attr=attr), 1)


def get_cameras():
    exclude = ["frontShape", "perspShape", "sideShape", "topShape"]
    cameras = mc.ls(cameras=1)
    cameras = list(set(cameras)-set(exclude))
    return cameras


if __name__ == "__main__":
    pass
