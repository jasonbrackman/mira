# -*- coding: utf-8 -*-
import os
import re
import logging
from miraLibs.pyLibs import join_path, get_latest_version_by_dir, get_latest_version_dir
from miraLibs.pipeLibs.pipeMira import get_root_dir, get_local_root_dir, get_vfx_cache_root_dir


type_dict = {"character": "char", "prop": "prop", "environment": "env"}


class PathError(Exception):
    pass


class PathDetails(object):
    def __init__(self):
        self.logger = logging.getLogger("pipeFile")
        self.project = None
        self.__is_working_file = False
        self.__is_publish_file = False
        self.__is_shd_file = False
        self.__is_gpu_file = False
        self.__is_local_file = False
        self.seq = None
        self.shot = None
        self.path_type = None
        self.asset_name = None
        self.asset_type = None
        self.asset_type_short_name = None
        self.category = None
        self.shd_version = None
        self.work_path = None
        self.publish_path = None
        self.image_path = None
        self.local_image_path = None
        self.video_path = None
        self.local_video_path = None
        self.gpu_cache_path = None
        self.context_version = None
        self.topology_path = None
        self.tex_dir = None
        self.hair_path = None
        self.cache_dir = None
        self.camera_dir = None
        self.camera_path = None
        self.env_path = None
        self.anim_render_path = None
        self.connection_path = None
        self.asset_info_path = None
        self.tempGeo_path = None
        self.uv_path = None
        self.sg_path = None
        self.current_version = None
        self.current_version_str = None
        self.next_version = None
        self.next_version_file = None
        self.other_dir = None

    @classmethod
    def parse_path(cls, path=None, only_workarea=True):
        x = cls()
        if not path:
            try:
                from miraLibs.mayaLibs import get_scene_name
                path = get_scene_name.get_scene_name()
            except:
                path = None
        if not path:
            x.logger.warning("Path is None")
            return None
        path = os.path.normpath(path)
        path = path.replace("\\", "/")
        # check file is local
        root_dir = os.path.splitdrive(path)[0]
        if root_dir in ["C:", "D:", "E:"]:
            x.__is_local_file = True
        path_base_name = os.path.basename(path)
        # check working file or publish file
        if "/_workarea/" in path:
            x.__is_working_file = True
        if "/_publish/" in path:
            x.__is_publish_file = True
        # get fields
        base_name_split_list = path_base_name.split("_")
        x.project = base_name_split_list[0]
        # -asset
        if len(base_name_split_list) == 4:
            x.path_type = "asset"
            x.asset_name = base_name_split_list[1]
            x.category = base_name_split_list[2]
            version_string = base_name_split_list[3].split(".")[0]
            x.current_version = int(version_string[1:])
            x.current_version_str = 'v' + str(x.current_version).zfill(3)
            x.next_version = x.current_version + 1
            x.next_version_file = re.sub("_v\d{3}\.", "_v%s." % str(x.next_version).zfill(3), path)
            x.next_version_file = x.next_version_file.replace("\\", "/")
            if x.category in ["shd"]:
                x.__is_shd_file = True
                x.shd_version = path.split("/")[-3]
            if "/character/" in path:
                x.asset_type = "character"
                x.asset_type_short_name = type_dict["character"]
            elif "/prop/" in path:
                x.asset_type = "prop"
                x.asset_type_short_name = type_dict["prop"]
            elif "/environment/" in path:
                x.asset_type = "environment"
                x.asset_type_short_name = type_dict["environment"]
        # -shot
        elif len(base_name_split_list) == 5:
            x.path_type = "shot"
            x.seq = base_name_split_list[1]
            x.shot = base_name_split_list[2]
            x.category = base_name_split_list[3]
            version_string = base_name_split_list[4].split(".")[0]
            x.current_version = int(version_string[1:])
            x.current_version_str = 'v' + str(x.current_version).zfill(3)
            x.next_version = x.current_version + 1
            x.next_version_file = re.sub("_v\d{3}\.", "_v%s." % str(x.next_version).zfill(3), path)
            x.next_version_file = x.next_version_file.replace("\\", "/")
        else:
            x.logger.warning("Invalid path...")
            return None
        if x.is_working_file():
            x.work_path = get_path(path)
            x.image_path = get_path(x.work_path, "_image", ".png",)
            x.local_image_path = get_path(path, "_image", ".png", None, True)
            x.video_path = get_path(x.work_path, "_video", ".mov")
            x.local_video_path = get_path(path, "_video", ".mov", None, True)
            x.publish_path = get_path(x.work_path, "_publish")
            other_dir = os.path.dirname(get_path(x.work_path, "_other"))
            x.other_dir = os.path.join(other_dir, x.current_version_str).replace("\\", "/")
            if x.category in ["shd", "hair"]:
                texture_dir = os.path.dirname(get_path(path, "_tex"))
                x.tex_dir = os.path.join(texture_dir, x.current_version_str).replace("\\", "/")
                x.hair_path = get_path(x.work_path, "_hair")
            if x.category == "mdl":
                x.gpu_cache_path = get_path(x.work_path, "_gpuCache", ".abc")
                x.topology_path = get_path(x.work_path, "_topology", ".json")
            if x.category in ["shd"]:
                x.connection_path = get_path(x.work_path, "_connection", ".json")
                x.uv_path = get_path(x.work_path, "_uv", ".json")
                x.sg_path = get_path(x.work_path, "_sg")
            if x.category == "sceneset":
                x.gpu_cache_path = get_path(x.work_path, "_gpuCache", ".abc")
                x.connection_path = get_path(x.work_path, "_connection", ".yml")
            if x.category == "lay":
                x.camera_path = get_path(x.work_path, "_camera", ".abc")
            if x.category == "anim":
                x.camera_path = get_path(x.work_path, "_camera", ".abc")
                x.anim_render_path = get_path(x.work_path, "_render")
                anim_cache_dir = os.path.dirname(get_path(x.work_path, "_cache"))
                x.cache_dir = os.path.join(anim_cache_dir, x.current_version_str).replace("\\", "/")
                x.env_path = get_path(x.work_path, "_env")
                x.asset_info_path = get_path(x.work_path, "_assetInfo", ".yml")
            if x.category == "sim":
                x.cache_dir = os.path.dirname(get_path(x.work_path, "_cache"))
        if x.category in ["lowRig", "rig", "shd", "hair"]:
            x.context_version = path.split(x.category)[1].split("/")[1]
        return x

    def is_working_file(self):
        return self.__is_working_file

    def is_publish_file(self):
        return self.__is_publish_file

    def is_shd_file(self):
        return self.__is_shd_file

    def is_gpu_file(self):
        return self.__is_gpu_file

    def is_local_file(self):
        return self.__is_local_file


def get_path(path, path_cate=None, ext=None, version=None, local=False):
    """
    get image/video/publish path from work path
    path: origin path/ source path
    path_cate: _image or _video or _publish
    ext: .jpg or .mov
    """
    project = os.path.basename(path).split("_")[0]
    root_dir = get_root_dir(project)
    local_root_dir = get_local_root_dir(project)
    driver = os.path.splitdrive(path)[0]
    if local:
        path = path.replace(driver, local_root_dir)
    else:
        path = path.replace(driver, root_dir)
    if path_cate:
        path = path.replace("_workarea", path_cate)
    if ext:
        path_ext = os.path.splitext(path)[-1]
        path = path.replace(path_ext, ext)
    if version is not None:
        path = re.sub("_v\d{3}\.", "_v%s." % str(version).zfill(3), path)
    return path


########################################################################################################################
# below is for get asset files
########################################################################################################################
def get_asset_step_dir(asset_type, asset_name, category, branch,
                       project_name=None, shd_version="default", rig_version="default", hair_version="default"):
    if not project_name:
        obj = PathDetails.parse_path()
        project_name = obj.project
    root_dir = get_root_dir(project_name)
    asset_step_dir = None
    if category in ["lowMdl", "mdl"]:
        asset_step_dir = join_path.join_path2(root_dir, project_name, "assets",
                                              asset_type, asset_name, category, branch)
    elif category in ["shd"]:
        asset_step_dir = join_path.join_path2(root_dir, project_name, "assets",
                                              asset_type, asset_name, category, shd_version, branch)
    elif category in ["lowRig", "rig"]:
        asset_step_dir = join_path.join_path2(root_dir, project_name, "assets",
                                              asset_type, asset_name, category, rig_version, branch)
    elif category in ["hair"]:
        asset_step_dir = join_path.join_path2(root_dir, project_name, "assets",
                                              asset_type, asset_name, category, hair_version, branch)
    return asset_step_dir


def get_asset_file(asset_type, asset_name, category, branch,
                   project_name=None, shd_version="default", rig_version="default", hair_version="default"):
    if not project_name:
        obj = PathDetails.parse_path()
        project_name = obj.project
    asset_publish_dir = get_asset_step_dir(asset_type, asset_name, category, branch,
                                           project_name, shd_version, rig_version, hair_version)
    if asset_publish_dir:
        asset_latest_publish_file = get_latest_version_by_dir.get_latest_version_by_dir(asset_publish_dir)
        if asset_latest_publish_file:
            asset_latest_publish_file = asset_latest_publish_file[0]
            return asset_latest_publish_file


def get_asset_step_publish_file(asset_type, asset_name, category, project_name=None,
                                shd_version="default", rig_version="default", hair_version="default"):
    asset_publish_file = get_asset_file(asset_type, asset_name, category,
                                        "_publish", project_name, shd_version, rig_version, hair_version)
    return asset_publish_file


def get_asset_step_workarea_file(asset_type, asset_name, category, project_name=None,
                                 shd_version="default", rig_version="default", hair_version="default"):
    asset_workarea_file = get_asset_file(asset_type, asset_name, category,
                                         "_workarea", project_name, shd_version, rig_version, hair_version)
    return asset_workarea_file


def get_asset_step_other_dir(asset_type, asset_name, category, project_name=None,
                             shd_version="default", rig_version="default", hair_version="default"):
    other_dir = get_asset_step_dir(asset_type, asset_name, category,
                                   "_other", project_name, shd_version, rig_version, hair_version)
    latest_other_dir = get_latest_version_dir.get_latest_version_dir(other_dir)
    return latest_other_dir


def get_asset_step_image_file(asset_type, asset_name, category, project_name=None,
                              shd_version="default", rig_version="default", hair_version="default"):
    path = get_asset_file(asset_type, asset_name, category,
                          "_image", project_name, shd_version, rig_version, hair_version)
    prefix, ext = os.path.splitext(path)
    asset_image_file = "%s.png" % prefix
    return asset_image_file


def get_asset_step_video_file(asset_type, asset_name, category, project_name=None,
                              shd_version="default", rig_version="default", hair_version="default"):
    path = get_asset_file(asset_type, asset_name, category,
                          "_video", project_name, shd_version, rig_version, hair_version)
    prefix, ext = os.path.splitext(path)
    asset_video_file = "%s.mov" % prefix
    return asset_video_file


########################################################################################################################
# below is for get shot files
########################################################################################################################
def get_shot_step_dir(sequence, shot, category, branch, project_name=None):
    if not project_name:
        obj = PathDetails.parse_path()
        project_name = obj.project
    root_dir = get_root_dir(project_name)
    shot_step_dir = join_path.join_path2(root_dir, project_name, "shots", sequence, shot, "3d", category, branch)
    return shot_step_dir


def get_shot_file(sequence, shot, category, branch, project_name=None):
    if not project_name:
        obj = PathDetails.parse_path()
        project_name = obj.project
    shot_publish_dir = get_shot_step_dir(sequence, shot, category, branch, project_name)
    asset_latest_publish_file = get_latest_version_by_dir.get_latest_version_by_dir(shot_publish_dir)
    if asset_latest_publish_file:
        asset_latest_publish_file = asset_latest_publish_file[0]
        return asset_latest_publish_file


def get_shot_step_workarea_file(sequence, shot, category, project_name=None):
    return get_shot_file(sequence, shot, category, "_workarea", project_name)


def get_shot_step_other_dir(sequence, shot, category, project_name=None):
    other_dir = get_shot_step_dir(sequence, shot, category, "_other", project_name)
    latest_other_dir = get_latest_version_dir.get_latest_version_dir(other_dir)
    return latest_other_dir


def get_shot_step_env_file(sequence, shot, category, project_name=None):
    return get_shot_file(sequence, shot, category, "_env", project_name)


def get_shot_step_publish_file(sequence, shot, category, project_name=None):
    return get_shot_file(sequence, shot, category, "_publish", project_name)


def get_shot_step_gpucache_file(sequence, shot, category, project_name=None):
    path = get_shot_file(sequence, shot, category, "_gpuCache", project_name)
    if not path:
        return
    prefix, ext = os.path.splitext(path)
    gpucache_path = "%s.abc" % prefix
    return gpucache_path


def get_shot_step_image_file(sequence, shot, category, project_name=None):
    path = get_shot_file(sequence, shot, category, "_image", project_name)
    if not path:
        return
    prefix, ext = os.path.splitext(path)
    image_path = "%s.png" % prefix
    return image_path


def get_shot_step_video_file(sequence, shot, category, project_name=None):
    path = get_shot_file(sequence, shot, category, "_video", project_name)
    if not path:
        return
    prefix, ext = os.path.splitext(path)
    video_path = "%s.mov" % prefix
    return video_path


def get_shot_step_connection_file(sequence, shot, category, project_name=None):
    path = get_shot_file(sequence, shot, category, "_connection", project_name)
    prefix, ext = os.path.splitext(path)
    connection_path = "%s.yml" % prefix
    return connection_path


def get_shot_step_assetinfo_file(sequence, shot, category, project_name=None):
    path = get_shot_file(sequence, shot, category, "_assetInfo", project_name)
    prefix, ext = os.path.splitext(path)
    connection_path = "%s.yml" % prefix
    return connection_path


def get_shot_step_camera_file(sequence, shot, category, project_name=None):
    camera_path = get_shot_file(sequence, shot, category, "_camera", project_name)
    return camera_path


def get_shot_step_anim_render_file(sequence, shot, project_name=None):
    anim_render_path = get_shot_file(sequence, shot, "anim", "_render", project_name)
    return anim_render_path


########################################################################################################################
# below is for get proxy files
########################################################################################################################


def get_proxy_dir(asset_name, project_name=None, sequence=None):
    if not project_name:
        obj = PathDetails.parse_path()
        project_name = obj.project
    root_dir = get_root_dir(project_name)
    if sequence:
        proxy_dir = join_path.join_path2(root_dir, project_name, "assets", "proxy", asset_name, "scene", sequence)
    else:
        proxy_dir = join_path.join_path2(root_dir, project_name, "assets", "proxy", asset_name, "static")
    return proxy_dir


########################################################################################################################
# below is for get vfx cache files
########################################################################################################################
def get_vfx_cache_dir(path=None):
    obj = PathDetails.parse_path(path)
    project_name = obj.project
    seq = obj.seq
    shot = obj.shot
    category = obj.category
    vfx_cache_root_dir = get_vfx_cache_root_dir(project_name)
    vfx_cache_dir = join_path.join_path2(vfx_cache_root_dir, project_name, "cache", seq, shot, category)
    vfx_cache_dir = vfx_cache_dir.replace("\\", "/")
    return vfx_cache_dir


if __name__ == "__main__":
    pass
