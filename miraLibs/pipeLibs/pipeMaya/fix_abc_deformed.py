# -*- coding: utf-8 -*-
import os
import logging
import tempfile
import shutil
import cask


logger = logging.getLogger(__name__)


def fix_abc_deformed(abc_path):
    tmp_file = tempfile.mktemp()
    logger.debug(tmp_file)
    shutil.copy2(abc_path, tmp_file)
    # parse abc
    abc_archive = cask.Archive(tmp_file)
    walk(abc_archive.top)
    abc_archive.write_to_file(abc_path)
    # delete temp file
    try:
        os.remove(tmp_file)
    except:pass


def walk(obj):
    if obj.type() == "PolyMesh" and obj.name.endswith("Deformed"):
        new_name = obj.name.rstrip("Deformed")
        obj.name = new_name
    for child in obj.children.values():
        walk(child)


if __name__ == "__main__":
    pass
