# -*- coding: utf-8 -*-
import os
import re
import logging
import join_path


def sort_key(text, length=10):
    str_num = "".join(re.findall("\d+", text))
    text = "".join(re.findall("\D", text)) + str_num.zfill(length)
    return text


def get_latest_version(path, offset=0):
    path = path.replace("\\", "/")
    dir_pattern = "/v\d+/"
    basename_pattern = ".*_v\d+\.\w+"
    base_name = os.path.basename(path)
    if re.match(basename_pattern, base_name) and not re.findall(dir_pattern, path):
        current_task_dir = os.path.dirname(path)
        if not os.path.isdir(current_task_dir):
            return
        padding_list = re.findall('_v(\d+)\.', path)
        if not padding_list:
            return
        padding = len(padding_list[0])
        path = path.replace('\\', '/')
        pattern = re.sub('_v\d{%s}\.' % padding, '_v(\d{%s})\.' % padding, path)
        # get all published versions
        versions = list()
        if not os.listdir(current_task_dir):
            max_version = 1
        else:
            for published_file in os.listdir(current_task_dir):
                published_file_path = os.path.join(current_task_dir, published_file).replace('\\', '/')
                matched = re.match(pattern, published_file_path)
                if not matched:
                    continue
                version_num = matched.group(1)
                versions.append(version_num)
            if versions:
                max_version = max([int(version) for version in versions])+offset
        max_version_str = '_v'+str(max_version).zfill(padding)+'.'
        publish_file_name = re.sub('_v\d{%s}\.' % padding, max_version_str, path)
        publish_file_name = os.path.abspath(publish_file_name)
        return publish_file_name, max_version
    elif re.findall(dir_pattern, path):
        version_dir = os.path.dirname(os.path.dirname(path))
        version_dir = version_dir.replace("\\", "/")
        versions = [version for version in os.listdir(version_dir) if re.match("v\d+", version)]
        versions = sorted(versions, key=lambda version: sort_key(version))
        max_version = versions[-1]
        version_num = int(max_version.split("v")[-1])
        max_version_num = version_num + offset
        max_version = "v%s" % str(max_version_num).zfill(3)
        max_version_file = join_path.join_path2(version_dir, max_version, base_name)
        return max_version_file, max_version_num
    else:
        logging.warning("not match standard file name.")
        return
