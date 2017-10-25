# -*- coding: utf-8 -*-
import logging
import os
import shutil
import tempfile

from miraLibs.mayaLibs import get_scene_name, save_file, open_file
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.backup import backup
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pipeLibs.pipeMaya.shd import export_shd_textures
from miraLibs.pyLibs import join_path


def main():
    logger = logging.getLogger(__name__)
    scene_name = get_scene_name.get_scene_name()
    # copy scene to temp dir
    base_name = os.path.basename(scene_name)
    temp_dir = tempfile.gettempdir()
    temp_file = join_path.join_path2(temp_dir, base_name)
    shutil.copy(scene_name, temp_file)
    logger.info("Copy to temp: %s" % temp_file)
    # copy all textures to _tex
    # if modified, backup it
    try:
        export_shd_textures.export_shd_textures()
    except:
        raise Exception("something wrong with export shd textures.")
    # save current file
    save_file.save_file()
    # copy to QCPublish path
    obj = pipeFile.PathDetails.parse_path()
    project = obj.project
    QCPublish_path = obj.QCPublish_path
    backup.backup(project, scene_name)
    Copy.copy(scene_name, QCPublish_path)
    logger.info("copy %s >> %s" % (scene_name, QCPublish_path))
    # copy from temp file
    shutil.copy(temp_file, scene_name)
    # delete temp file
    os.remove(temp_file)
    # open scene name
    open_file.open_file(scene_name)
    logger.info("Reopen %s" % scene_name)
