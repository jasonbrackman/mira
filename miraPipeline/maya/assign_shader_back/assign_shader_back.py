# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraLibs.pipeLibs.pipeMaya import assign_shader, get_asset_names
reload(assign_shader)


def assign_shader_back():
    assets = get_asset_names.get_asset_names()
    for asset in assets:
        assign_shader.assign_shader(asset)
    QMessageBox.information(None, "Warming Tip", "Assign shader done.")


if __name__ == "__main__":
    assign_shader_back()
