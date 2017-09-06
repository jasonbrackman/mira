import maya.cmds as mc
import os
from miraLibs.pyLibs import copy


LOCAL_DIR = "D:/vender"


def get_all_ar_files():
    files = list()
    ar_nodes = mc.ls(type="assemblyReference")
    if ar_nodes:
        for node in ar_nodes:
            reps = mc.assembly(node, q=1, listRepresentations=1)
            if not reps:
                continue
            for index, rep in enumerate(reps):
                file_path = mc.getAttr("%s.rep[%s].rda" % (node, index))
                files.append(file_path)
    return files


def get_all_reference_files():
    reference_files = list()
    all_ref = mc.ls(type='reference')
    references = [ref for ref in all_ref if 'sharedReferenceNode' not in ref]
    if references:
        for ref in references:
            ref_file = mc.referenceQuery(ref, filename=1, wcn=1)
            reference_files.append(ref_file)
    return reference_files


def package_file():
    ar_files = get_all_ar_files()
    ref_files = get_all_reference_files()
    all_files = ar_files + ref_files
    all_files = list(set(all_files))
    for f in all_files:
        if not os.path.isfile(f):
            print "%s is not an exist file" % f
            continue
        driver, suffix = os.path.splitdrive(f)
        new_path = "%s/%s" % (LOCAL_DIR, suffix)
        copy.copy(f, new_path)
        print "copy %s >> %s" % (f, new_path)


if __name__ == "__main__":
    package_file()
