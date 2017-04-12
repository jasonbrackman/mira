# -*- coding: utf-8 -*-
import os


def get_children_files(file_path, ext_list):
    file_path = file_path.replace("\\", "/")
    if isinstance(ext_list, basestring):
        ext_list = [ext_list]
    all_files = list()
    if os.path.isfile(file_path) and os.path.splitext(file_path)[-1] in ext_list:
        all_files.append(file_path)
    elif os.path.isdir(file_path):
        for root, dirs, files in os.walk(file_path):
            if not dirs:
                for f in files:
                    file_full_path = os.path.join(root, f)
                    file_full_path = file_full_path.replace("\\", "/")
                    if os.path.splitext(file_full_path)[-1] in ext_list:
                        all_files.append(file_full_path)
    return all_files



