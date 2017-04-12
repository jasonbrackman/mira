import pymel.core as pm
import get_selected_objects


def get_sg_node_of_mesh(mesh):
    return mesh.outputs(type='shadingEngine')


def get_sg_node_of_selected():
    sg_nodes = []
    all_meshes = get_selected_objects.get_selected_objects()
    if all_meshes:
        for mesh in all_meshes:
            sg_nodes.extend(get_sg_node_of_mesh(mesh))
        sg_nodes = list(set(sg_nodes))
        return sg_nodes
    else:
        return None