# -*- coding: utf-8 -*-
import logging
import get_all_meshes
import get_sg_node_of_mesh


def get_all_used_sg():
    logger = logging.getLogger(__name__)
    meshes = get_all_meshes.get_all_meshes()
    all_sg_nodes = list()
    invalid_meshes = list()
    for mesh in meshes:
        sg_nodes = get_sg_node_of_mesh.get_sg_node_of_mesh(mesh)
        if not sg_nodes:
            continue
        if not len(sg_nodes) == 1:
            invalid_meshes.append(mesh.longName())
        all_sg_nodes.append(sg_nodes[0])
    if invalid_meshes:
        error_info = "These meshes have wrong shader connection:\n%s" % "\n".join(invalid_meshes)
        logger.error(error_info)
        return
    else:
        return all_sg_nodes


if __name__ == "__main__":
    pass
