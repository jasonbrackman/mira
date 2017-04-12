# -*- coding: utf-8 -*-
import pymel.core as pm
from miraLibs.mayaLibs import get_all_meshes


def export_meshes_without_shader(mdl_path, maya_type="mayaBinary"):
    """
    export all the meshes without shader, for the model last publish and last work file
    :return:
    """
    all_meshes = get_all_meshes.get_all_meshes()
    default_sg = pm.PyNode("initialShadingGroup")
    pm.sets(default_sg, fe=all_meshes)
    pm.select(all_meshes, r=1, ne=1)
    pm.exportSelected(mdl_path, type=maya_type, force=1)


if __name__ == "__main__":
    pass
