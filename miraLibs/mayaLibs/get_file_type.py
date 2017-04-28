# -*- coding: utf-8 -*-


def get_file_type(path):
    file_type = None
    if path.endswith(".abc"):
        file_type = "Alembic"
    elif path.endswith(".mb"):
        file_type = "mayaBinary"
    elif path.endswith(".ma"):
        file_type = "mayaAscii"
    return file_type
