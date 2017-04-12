import maya.cmds as mc
import os
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_namespace, export_exocortex_abc, get_frame_range
from miraLibs.pipeLibs.pipeMaya.get_assets_under_type_group import get_assets_under_type_group


def export_single_abc(asset):
    obj = pipeFile.PathDetails.parse_path()
    mc.parent(asset, world=1)
    namespace = get_namespace.get_namespace(asset)
    abc_name = "%s.abc" % namespace
    abc_path = os.path.join(obj.cache_dir, abc_name).replace("\\", "/")
    start, end = get_frame_range.get_frame_range()
    meshes = mc.listRelatives(asset, ad=1, type="mesh")
    geo = [mc.listRelatives(mesh, p=1)[0] for mesh in meshes]
    objects = list(set(geo))
    export_exocortex_abc.export_exocortex_abc(abc_path, 1, end, objects)


def export_model_abc():
    assets = get_assets_under_type_group("char")+get_assets_under_type_group("prop")
    if not assets:
        return
    for asset in assets:
        export_single_abc(asset)


if __name__ == "__main__":
    export_model_abc()
