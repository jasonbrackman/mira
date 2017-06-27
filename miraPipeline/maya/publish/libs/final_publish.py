# -*- coding: utf-8 -*-
from miraLibs.pyLibs.copy import copy


class FinalCopier(object):
    def __init__(self, obj):
        self.obj = obj

    def copy_image(self):
        copy(self.obj.image_path, self.obj.final_image_path)

    def copy_video(self):
        copy(self.obj.video_path, self.obj.final_video_path)

    def copy_publish_file(self):
        copy(self.obj.publish_path, self.obj.final_path)

    def copy_asset_cache(self):
        copy(self.obj.abc_cache_path, self.obj.final_cache_path)

    def copy_topology(self):
        copy(self.obj.topology_path, self.obj.final_topology_path)


class FinalPublish(object):
    def __init__(self, obj):
        self.obj = obj
        self.copier = FinalCopier(self.obj)
        self.step = self.obj.step

    def publish(self):
        self.copier.copy_image()
        if self.step == "MidMdl":
            self.copier.copy_video()
            self.copier.copy_publish_file()
            self.copier.copy_asset_cache()
