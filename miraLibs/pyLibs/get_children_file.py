# -*- coding: utf-8 -*-
import logging
import os
import join_path


def get_children_file(file_dir, ext=None):
    logger = logging.getLogger(__name__)
    file_dir = file_dir.replace("\\", "/")
    if not os.path.isdir(file_dir):
        logger.warning("%s is not an exist dir." % file_dir)
        return
    if not ext:
        children_files = [join_path.join_path2(file_dir, f) for f in os.listdir(file_dir)
                          if os.path.isfile(join_path.join_path2(file_dir, f))]
    else:
        if isinstance(ext, basestring):
            ext = [ext]
        if not isinstance(ext, list):
            logger.error("arg: ext must be a type of list.")
            return
        children_files = [join_path.join_path2(file_dir, f) for f in os.listdir(file_dir)
                          if os.path.isfile(join_path.join_path2(file_dir, f)) and os.path.splitext(f)[-1] in ext]
    return children_files
