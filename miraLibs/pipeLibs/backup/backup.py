# -*- coding: utf-8 -*-
import logging
import os
import re
from miraLibs.pipeLibs import pipeMira
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pyLibs import join_path, copy


def backup(project, file_path, permission=False):
    logger = logging.getLogger(__name__)
    if not os.path.isfile(file_path):
        logger.warning("%s is not an exist file." % file_path)
        return
    file_base_name = os.path.basename(file_path)
    current_root_dir = os.path.splitdrive(file_path)[0]
    backup_root_dir = pipeMira.get_backup_dir(project)
    backup_file = file_path.replace(current_root_dir, backup_root_dir)
    backup_file = Copy.convert_dir(backup_file)
    backup_dir = os.path.dirname(backup_file)
    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)
    if not os.listdir(backup_dir):
        backup_file = re.sub(r"_v\d{3}\.", "_v000.", backup_file)
        my_copy(file_path, backup_file, permission)
        logger.info("backup %s >> %s" % (file_path, backup_file))
        return
    pattern = re.sub(r"_v\d{3}\.", "_v(\d{3}).", file_base_name)
    versions = list()
    matched_files = list()
    for f in os.listdir(backup_dir):
        matched = re.match(pattern, f)
        if not matched:
            continue
        current_version = matched.group(1)
        versions.append(current_version)
        matched_files.append(f)
    if not matched_files:
        backup_file = re.sub(r"_v\d{3}\.", "_v000.", backup_file)
        my_copy(file_path, backup_file, permission)
        logger.info("backup %s >> %s" % (file_path, backup_file))
        return
    int_versions = [int(version) for version in versions]
    max_version = max(int_versions)
    next_version = str(max_version+1).zfill(3)
    next_version_file = re.sub(r"_v\d{3}\.", "_v%s." % str(next_version).zfill(3), matched_files[0])
    new_file_path = join_path.join_path2(backup_dir, next_version_file)
    my_copy(file_path, new_file_path, permission)
    logger.info("backup %s >> %s" % (file_path, new_file_path))


def my_copy(src, dst, permission=False):
    if permission:
        copy.copy(src, dst)
    else:
        Copy.copy(src, dst)


if __name__ == "__main__":
    backup("sct", r"D:\sct\assets\character\newbee\mdl\_workarea\sct_newbee_mdl_v010.mb")