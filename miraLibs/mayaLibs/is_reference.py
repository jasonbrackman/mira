# -*- coding: utf-8 -*-
import pymel.core as pm


def is_reference(node):
    return pm.referenceQuery(node, isNodeReferenced=1)


if __name__ == "__main__":
    pass
