# -*- coding: utf-8 -*-
import os
import re
import logging
from miraLibs.pyLibs import join_path


def get_texture_real_path(texture):
    logger = logging.getLogger(__name__)
    real_texture = list()
    if "<udim>" in texture or "<UDIM>" in texture:
        texture_dir, texture_base_name = os.path.split(texture)
        pattern = texture_base_name.replace("<udim>", "\d{4}")
        pattern = pattern.replace("<UDIM>", "\d{4}")
        for i in os.listdir(texture_dir):
            if re.match(pattern, i):
                full_name = join_path.join_path2(texture_dir, i)
                real_texture.append(full_name)
    elif os.path.isfile(texture):
        real_texture.append(texture)
    else:
        logger.warning("%s is not an exist file." % texture)
    return real_texture
