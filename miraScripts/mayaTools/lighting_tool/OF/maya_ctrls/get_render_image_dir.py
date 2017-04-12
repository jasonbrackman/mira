__author__ = 'heshuai'


import os
import maya.cmds as mc
import get_os_type


def get_render_image_dir():
    os_type = get_os_type.get_os_type()
    final_dir = None
    try:
        full_path = mc.renderSettings(firstImageName=1, fullPath=1)[0]
        image_dir = full_path.split('images')[0]
        acc_dir = os.path.dirname(full_path.split('images')[1].strip('/'))
        tmp_dir = os.path.join(image_dir, 'images', 'tmp')
        new_image_dir = os.path.join(tmp_dir, acc_dir)
        new_image_dir = new_image_dir.replace('\\', '/')
        if os.path.isdir(new_image_dir):
            final_dir = new_image_dir
        elif os.path.isdir(tmp_dir):
            final_dir = tmp_dir
        elif os.path.isdir(image_dir):
            final_dir = image_dir
    except:
        full_path = mc.renderSettings(firstImageName=1, fullPathTemp=1)[0]
        final_dir = os.path.dirname(full_path)
    print final_dir
    if os.path.isdir(final_dir):
        if os_type == 'windows':
            os.startfile(final_dir)
        if os_type == 'linux':
            os.system('xdg-open %s' % final_dir)