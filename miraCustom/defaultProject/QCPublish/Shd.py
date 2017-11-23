# -*- coding: utf-8 -*-
import logging
import os
import tempfile
from miraLibs.mayaLibs import get_scene_name, save_file, open_file
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.copy import Copy
from miraLibs.pipeLibs.pipeMaya.shd import export_shd_textures
from miraLibs.pyLibs import join_path, copy
from miraLibs.pyLibs.image import resize_image


def main():
    logger = logging.getLogger(__name__)
    scene_name = get_scene_name.get_scene_name()
    # copy scene to temp dir
    base_name = os.path.basename(scene_name)
    temp_dir = tempfile.gettempdir()
    temp_file = join_path.join_path2(temp_dir, base_name)
    copy.copy(scene_name, temp_file)
    logger.info("Copy to temp: %s" % temp_file)
    # copy all textures to _tex
    try:
        export_shd_textures.export_shd_textures()
    except:
        raise Exception("something wrong with export shd textures.")
    # save current file
    save_file.save_file()
    # copy to QCPublish path
    context = pipeFile.PathDetails.parse_path()
    work_path = context.work_path
    # convert image
    convert_image(context)
    logger.info("Convert image done.")
    if Copy.copy(scene_name, work_path):
        logger.info("copy %s >> %s" % (scene_name, work_path))
    else:
        raise RuntimeError("copy to work path error.")
    # copy from temp file
    copy.copy(temp_file, scene_name)
    logger.info("copy from temp.")
    # delete temp file
    os.remove(temp_file)
    # open scene name
    open_file.open_file(scene_name)
    logger.info("Reopen %s" % scene_name)


def convert_image(context):
    tex_dir = context.tex_dir
    ext_list = [".tif", ".tiff", ".png", ".tga", ".jpg", ".jpeg", ".exr", ".psd", ".bmp"]
    for i in os.listdir(tex_dir):
        tex_name = "%s/%s" % (tex_dir, i)
        if not os.path.isfile(tex_name):
            continue
        ext = os.path.splitext(tex_name)[-1]
        if ext not in ext_list:
            continue
        prefix, suffix = os.path.split(tex_name)
        half_tex_name = "%s/half/%s" % (prefix, suffix)
        half_tex_dir = os.path.dirname(half_tex_name)
        if not os.path.isdir(half_tex_dir):
            os.makedirs(half_tex_dir)
        resize_image(tex_name, half_tex_name)


if __name__ == "__main__":
    pass
