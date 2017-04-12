# -*- coding: utf-8 -*-
import pymel.core as pm
from miraLibs.pyLibs import get_new_version


def aas_save_as(file_path=None):
    # get current name
    if not file_path:
        file_path = pm.sceneName()
    if not file_path:
        pm.mel.eval("SaveSceneAs;")
        return
    file_path = str(file_path)
    # get new version
    new_version_info = get_new_version.get_new_version(file_path)
    if not new_version_info:
        pm.mel.eval("SaveSceneAs;")
        return

    # get new file name
    new_version_path = new_version_info[0]
    pm.saveAs(new_version_path, force=True)


if __name__ == "__main__":
    pass
