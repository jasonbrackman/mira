# -*- coding: utf-8 -*-
import os
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import export_gpu_cache, open_file
from miraLibs.stLibs import St

st = St.St("SnowKidTest")
assets = st.get_all_assets("Prop")

prop_assets = [asset.get("name") for asset in assets if asset.get("name").startswith("SSWH")]


for asset in prop_assets:
    publish_path = pipeFile.get_task_publish_file("SnowKidTest", "Asset", "Prop", asset, "MidMdl", "MidMdl")
    if not os.path.isfile(publish_path):
        continue
    open_file.open_file(publish_path)
    context = pipeFile.PathDetails.parse_path(publish_path)
    model_name = "%s_%s_MODEL" % (context.asset_type_short_name, context.asset_name)
    directory = os.path.dirname(context.abc_cache_path)
    filename = os.path.splitext(os.path.basename(context.abc_cache_path))[0]
    export_gpu_cache.export_gpu_cache(model_name, directory, filename)
    print "%s export abc done." % asset

