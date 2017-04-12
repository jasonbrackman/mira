# -*- coding: utf-8 -*-
import pymel.core as pm
import load_plugin


def create_reference(path, namespace_name=":", allow_repeat=False, get_group=False):
    result = None
    path = path.replace("\\", "/")
    if path.endswith(".abc"):
        load_plugin.load_plugin("AbcImport.mll")
    file_type = get_file_type(path)
    if allow_repeat:
        result = pm.system.createReference(path, loadReferenceDepth="all",
                                           mergeNamespacesOnClash=False,
                                           namespace=namespace_name,
                                           type=file_type)
    else:
        references = pm.listReferences()
        if not references:
            print "*"*100
            result = pm.system.createReference(path, loadReferenceDepth="all",
                                               ignoreVersion=1, gl=1,
                                               options="v=0",
                                               mergeNamespacesOnClash=True,
                                               namespace=namespace_name,
                                               type=file_type)
        else:
            reference_paths = [ref.path for ref in references]
            if path not in reference_paths:
                result = pm.system.createReference(path, loadReferenceDepth="all",
                                                   mergeNamespacesOnClash=True,
                                                   namespace=namespace_name,
                                                   type=file_type)
            else:
                ref_node = pm.referenceQuery(path, referenceNode=1)
                if not pm.referenceQuery(ref_node, isLoaded=1):
                    pm.system.loadReference(path)
    if get_group:
        return pm.referenceQuery(result.refNode, dagPath=1, nodes=1)[0]


def get_file_type(path):
    file_type = None
    if path.endswith(".abc"):
        file_type = "Alembic"
    elif path.endswith(".mb"):
        file_type = "mayaBinary"
    elif path.endswith(".ma"):
        file_type = "mayaAscii"
    return file_type


if __name__ == "__main__":
    pass
