# -*- coding: utf-8 -*-
import pymel.core as pm
from miraLibs.pyLibs import get_latest_version


def update_reference(ref_node):
    path = ref_node.referenceFile().path.replace("/", "\\")
    latest_version = get_latest_version.get_latest_version(path)[0]
    if path != latest_version:
        rn = pm.system.FileReference(ref_node)
        rn.replaceWith(latest_version)
