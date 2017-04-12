import maya.cmds as mc
from miraLibs.mayaLibs import get_shader_history_nodes


def get_all_hair_file_node():
    hair_shaders = mc.ls(type=["aiHair", "RedshiftHair"])
    all_nodes = list()
    file_nodes = list()
    for shader in hair_shaders:
        history_node = get_shader_history_nodes.get_shader_history_nodes(shader, False)
        all_nodes.extend(history_node)
    if all_nodes:
        all_nodes = list(set(all_nodes))
        file_nodes = mc.ls(all_nodes, type="file")
    return file_nodes
