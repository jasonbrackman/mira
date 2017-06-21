# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraLibs.pyLibs import join_path


def get_proxy_dir():
    obj = pipeFile.PathDetails.parse_path()
    project = obj.project
    asset_name = obj.asset_name
    root_dir = pipeMira.get_root_dir(project)
    proxy_dir = join_path.join_path2(root_dir, project, "assets", "proxy", asset_name, "static")
    return proxy_dir


def export_ass():
    proxy_dir = get_proxy_dir()
    meshes = mc.ls(type="mesh", long=1)
    progress_dialog = QProgressDialog("Ass Exporting...", 'Cancel', 0, len(meshes))
    progress_dialog.setWindowModality(Qt.WindowModal)
    progress_dialog.setMinimumWidth(350)
    progress_dialog.show()
    for index, mesh in enumerate(meshes):
        progress_dialog.setValue(index)
        if progress_dialog.wasCanceled():
            break
        mc.select(mesh, r=1)
        new_name = mesh.replace("|", "@")
        mc.file(os.path.join(proxy_dir, "%s.ass" % new_name),
                options="-mask 8;-lightLinks 0;-boundingBox;-shadowLinks 0",
                f=1, type="ASS Export", shader=0, exportSelected=1)


if __name__ == "__main__":
    export_ass()
