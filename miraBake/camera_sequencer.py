# -*- coding: utf-8 -*-
import os
import re
import logging
import maya.cmds as mc
from miraLibs.pyLibs import join_path

logger = logging.getLogger(__name__)


def get_xml_path():
    # TODO\
    xml_path = r"Z:\Shotgun\projects\df\animatic\seq001\df_001_sb.xml"
    return xml_path


def import_xml(xml_path):
    import maya.app.edl.importExport as EDL
    EDL.doImport(xml_path, 0, 1)


def fix_image_settings(xml_path):
    mov_dir = os.path.abspath(os.path.dirname(xml_path))
    image_shapes = mc.ls(type="imagePlane")
    attr_name = "mov_path"
    for image_shape in image_shapes:
        image_name = mc.getAttr("%s.imageName" % image_shape)
        if not image_name:
            shot_nodes = mc.listConnections(image_shape, s=0, d=1, type="shot")
            image_name = "%s.mov" % shot_nodes[0]
        new_image_path = join_path.join_path2(mov_dir, os.path.basename(image_name))
        mc.setAttr("%s.imageName" % image_shape, new_image_path, type="string")
        if not mc.ls("%s.%s" % (image_shape, attr_name)):
            mc.addAttr(image_shape, ln=attr_name, dt="string")
        mc.setAttr("%s.%s" % (image_shape, attr_name), new_image_path, type="string")


def fix_audio_settings(xml_path):
    wav_dir = os.path.dirname(xml_path)
    audios = mc.ls(type="audio")
    for audio in audios:
        # rename audio
        shot_name = mc.listConnections(audio, s=0, d=1, type="shot")
        if not shot_name:
            logger.warning("%s has no shot connected" % shot_name)
            continue
        new_audio_name = "%s_audio" % shot_name[0]
        mc.rename(audio, new_audio_name)
        # set audio file name
        audio_file_name = join_path.join_path2(wav_dir, "%s.wav" % shot_name[0])
        if os.path.isfile(audio_file_name):
            mc.setAttr("%s.filename" % new_audio_name, audio_file_name, type="string")
        else:
            logger.warning("%s is not exist" % audio_file_name)


def fix_camera_settings():
    pattern = "\w+_(\d+\w?_\d+\w?)_\w+"
    for shot_name in mc.ls(type="shot"):
        # shot_name format: df_001_004_sb
        if not re.match(pattern, shot_name):
            logger.warning("%s is not a valid name shot" % shot_name)
            continue
        else:
            cut_name = re.match(pattern, shot_name).group(1)
            cameras = mc.listConnections(shot_name, s=1, d=0, type="camera")
            if cameras:
                camera = cameras[0]
                new_camera_name = "cam_%s" % cut_name
                mc.rename(camera, new_camera_name)
            else:
                logger.error("%s has no camera connected" % shot_name)
    # set camera display settings
    for camera in mc.ls(type="camera"):
        if camera not in ["frontShape", "perspShape", "sideShape", "topShape"]:
            mc.setAttr("%s.displayGateMaskColor" % camera, 0, 0, 0, type="double3")
            mc.setAttr("%s.displayGateMaskOpacity" % camera, 1)
            mc.setAttr("%s.displayResolution" % camera, 1)
            mc.setAttr("%s.overscan" % camera, 1.15)


def fix_time_line():
    start_frames = list()
    end_frames = list()
    for shot_name in mc.ls(type="shot"):
        start_frame = mc.getAttr("%s.startFrame" % shot_name)
        end_frame = mc.getAttr("%s.endFrame" % shot_name)
        start_frames.append(start_frame)
        end_frames.append(end_frame)
    min_frame = min(start_frames)
    max_frame = max(end_frames)
    mc.playbackOptions(e=1, min=min_frame)
    mc.playbackOptions(e=1, max=max_frame)
    mc.playbackOptions(e=1, ast=min_frame)
    mc.playbackOptions(e=1, aet=max_frame)


def main():
    xml_path = get_xml_path()
    # import xml
    import_xml(xml_path)
    # rename camera
    fix_camera_settings()
    # add image settings
    fix_image_settings(xml_path)
    # audio settings
    fix_audio_settings(xml_path)
    # fix time line
    fix_time_line()
