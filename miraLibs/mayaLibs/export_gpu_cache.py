# -*- coding: utf-8 -*-
import maya.cmds as mc


def export_gpu_cache(root, directory, filename, start_time, end_time, save_multiple_files=True):
    mc.gpuCache(root, directory=directory, fileName=filename,
                startTime=start_time, endTime=end_time, saveMultipleFiles=save_multiple_files)
