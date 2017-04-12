# -*- coding: utf-8 -*-
import pymel.core as pm
import get_all_used_sg


def export_all_used_sg(shader_path, maya_type="mayaBinary"):
    """
    export all the used shadingEngine nodes in this maya file
    :return:
    """
    all_sg_nodes = get_all_used_sg.get_all_used_sg()
    pm.select(all_sg_nodes, r=1, ne=1)
    pm.exportSelected(shader_path, type=maya_type, force=1)


if __name__ == "__main__":
    pass
