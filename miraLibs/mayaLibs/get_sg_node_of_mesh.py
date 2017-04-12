# -*- coding: utf-8 -*-


def get_sg_node_of_mesh(mesh):
    sg_nodes = mesh.outputs(type="shadingEngine")
    return sg_nodes


if __name__ == "__main__":
    pass
