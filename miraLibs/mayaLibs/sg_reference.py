# -*- coding: utf-8 -*-

import pymel.core as pm
import os
import re


def sg_reference(entity_name, path):
    pattern = '(.*)_v\d+\.m[ab]$'
    task_file_name = os.path.basename(path)
    matched = re.findall(pattern, task_file_name)
    if matched:
        task_file_name = matched[0]
    namespace = "%s %s" % (entity_name, task_file_name)
    namespace = namespace.replace(" ", "_")
    pm.system.createReference(path,
                              loadReferenceDepth="all",
                              mergeNamespacesOnClash=False,
                              namespace=namespace)


if __name__ == "__main__":
    pass
