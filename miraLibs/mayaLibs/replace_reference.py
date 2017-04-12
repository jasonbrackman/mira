# -*- coding: utf-8 -*-
import pymel.core as pm


def replace_reference(ref_node, ref_path):
    rn = pm.system.FileReference(ref_node)
    rn.replaceWith(ref_path)
