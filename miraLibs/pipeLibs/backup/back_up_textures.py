# -*- coding: utf-8 -*-
import os
import logging
import filecmp
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pyLibs import join_path


def back_up_textures(backup_tex_dir, file_path, scene_version=None):
    file_path = file_path.replace("\\", "/")
    logger = logging.getLogger(__name__)
    if not os.path.isfile(file_path):
        logger.warning("%s is not an exist file." % file_path)
        return
    base_name = os.path.basename(file_path)
    backup_file = join_path.join_path2(backup_tex_dir, base_name)
    if not os.path.isfile(backup_file):
        Copy.copy(file_path, backup_file)
        logger.info("backup %s >> %s" % (file_path, backup_file))
    else:
        if not filecmp.cmp(file_path, backup_file):
            base_name = os.path.basename(backup_file)
            version_str = "v"+str(scene_version).zfill(3)
            s_base_name, ext = os.path.splitext(base_name)
            new_base_name = "%s_%s%s" % (s_base_name, version_str, ext)
            new_backup_file = join_path.join_path2(backup_tex_dir, new_base_name)
            Copy.copy(file_path, new_backup_file)
            logger.info("backup %s >> %s" % (file_path, new_backup_file))
