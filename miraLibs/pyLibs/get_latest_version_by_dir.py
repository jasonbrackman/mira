# -*- coding: utf-8 -*-
import os
import re
import logging
import join_path

logger = logging.getLogger(__name__)


def get_latest_version_by_dir(directory, offset=0):
    directory = directory.replace("\\", "/")
    if not os.path.isdir(directory):
        return
    if not os.listdir(directory):
        logger.info("No file exist in %s" % directory)
        return
    pattern = "_v(\d+)."
    version_files = [f for f in os.listdir(directory) if re.findall(pattern, f)]
    if not version_files:
        print "No file matched _v\d+."
        return
    max_version = -1
    max_version_file = None
    for version_file in version_files:
        version_num = int(re.findall(pattern, version_file)[0])
        if version_num > max_version:
            max_version = version_num
            max_version_file = version_file
    if max_version_file:
        if offset == 0:
            max_version_file_path = join_path.join_path2(directory, max_version_file)
            return max_version_file_path, max_version
        else:
            padding = len(re.findall(pattern, version_files[0])[0])
            max_version += offset
            new_version_file = re.sub("_v\d{%s}\." % padding,
                                      "_v"+str(max_version).zfill(padding)+".", version_files[0])
            new_version_file_path = join_path.join_path2(directory, new_version_file)
            return new_version_file_path, max_version


if __name__ == "__main__":
    pass


