# -*- coding: utf-8 -*-
from miraLibs.mayaLibs import export_abc, get_frame_range


def export_camera_abc(seq, shot, camera_path, attribute=None):
    camera_name = "cam_%s_%s" % (seq, shot)
    start_frame, end_frame = get_frame_range.get_frame_range()
    export_abc.export_abc(start_frame, end_frame, camera_path, camera_name, False, attribute=attribute)
