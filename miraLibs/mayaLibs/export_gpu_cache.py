# -*- coding: utf-8 -*-
import maya.cmds as mc


def export_gpu_cache(root, directory, filename, start_time=1, end_time=1, save_multiple_files=True):
    mc.gpuCache(root, directory=directory, fileName=filename, optimize=1, writeMaterials=1, dataFormat="ogawa",
                startTime=start_time, endTime=end_time, saveMultipleFiles=save_multiple_files)
