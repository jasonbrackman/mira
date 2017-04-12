# -*- coding: utf-8 -*-
import pymel.core as pm
import is_reference


def get_namespace(node):
    if is_reference.is_reference(node):
        namespace = pm.referenceQuery(node, namespace=1)
        if namespace == ":":
            namespace = ":".join(node.split(":")[:-1])
    else:
        namespace = ":".join(node.split(":")[:-1])
    return namespace.strip(":")


if __name__ == "__main__":
    pass
