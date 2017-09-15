# -*- coding: utf-8 -*-
import os
import re
import logging
from miraLibs.pyLibs.Path import Path
from miraLibs.pyLibs import opposite_format, get_latest_version
from miraLibs.pipeLibs.pipeMira import get_projects, get_local_root_dir, get_primary_dir, get_studio_value


type_dict = {"Character": "char", "Prop": "prop", "Cprop": "cprop", "Environment": "env", "Building": "build"}


def get_entity_type(path):
    if "/assets/" in path:
        entity_type = "Asset"
    elif "/shots/" in path:
        entity_type = "Shot"
    else:
        return
    return entity_type


def get_project(path):
    base_name = Path(path).basename()
    project = base_name.split("_")[0]
    if project in get_projects():
        return project


class PathDetails(object):
    def __init__(self):
        self.logger = logging.getLogger("pipeFile")
        self.path = None
        self.entity_type = None
        self.edition = None
        self.version_format_spec = None
        self.edition_format_spec = None
        self.__is_local_file = False
        self.__is_working_file = False
        self.__is_publish_file = False

    @classmethod
    def parse_path(cls, path=None):
        x = cls()
        if not path:
            try:
                from miraLibs.osLibs import get_scene_name
                path = get_scene_name.get_scene_name()
            except:
                path = None
        if not path:
            x.logger.warning("Path is None")
            return None
        path_obj = Path(path)
        path = path_obj.regular()
        x.path = path
        x.entity_type = get_entity_type(path)
        project = get_project(path)
        if not project:
            return
        if x.entity_type == "Asset":
            template = get_studio_value(project, "asset_template")
        else:
            template = get_studio_value(project, "shot_template")
        context_dict = opposite_format.opposite_format(template, path)
        if not context_dict:
            return x
        x.__dict__.update(context_dict)
        if x.area == "_workarea":
            x.__is_working_file = True
        elif x.area == "_publish":
            x.__is_publish_file = True
        if hasattr(x, "version"):
            if "_e" in x.version:
                x.__is_local_file = True
                x.version, x.edition = x.version.split("_e")
                x.edition_format_spec = len(x.edition)
                x.version_format_spec = len(x.version)
        else:
            x.version = ""
        if x.entity_type == "Asset":
            x.asset_type_short_name = type_dict[x.asset_type]
        return x

    def is_working_file(self):
        return self.__is_working_file

    def is_publish_file(self):
        return self.__is_publish_file

    def is_local_file(self):
        return self.__is_local_file

    def as_template(self, format_area, local=False):
        if not self.edition:
            self.edition = "000"
        if self.entity_type == "Asset":
            format_str = "%s_asset_%s" % (self.engine, format_area)
            return get_task_file(self.project, self.asset_type, self.asset_name, self.step, self.task,
                                 format_str, self.version, self.engine, local, self.edition)
        else:
            format_str = "%s_shot_%s" % (self.engine, format_area)
            return get_task_file(self.project, self.sequence, self.shot, self.step, self.task,
                                 format_str, self.version, self.engine, local, self.edition)

    @property
    def next_version(self):
        next_version = str(int(self.version) + 1).zfill(len(self.version))
        return next_version

    @property
    def next_edition(self):
        if self.is_local_file():
            next_edition = str(int(self.edition) + 1).zfill(len(self.edition))
            return next_edition

    @property
    def next_version_file(self):
        if self.is_local_file():
            next_version_file = re.sub("_v\d{%s}_e\d{%s}\." % (self.version_format_spec, self.edition_format_spec),
                                       "_v%s_e%s." % (self.next_version, str(0).zfill(self.edition_format_spec)),
                                       self.path)
        else:
            next_version_file = re.sub("_v\d{%s}\." % self.version_format_spec, "_v%s." % self.next_version, self.path)
        return next_version_file

    @property
    def next_edition_file(self):
        if self.is_local_file():
            next_edition_file = re.sub("_e\d{%s}\." % self.edition_format_spec, "_e%s." % self.next_edition, self.path)
            return next_edition_file
        
    @property
    def task_info(self):
        from miraLibs.dbLibs import db_api
        db = db_api.DbApi(self.project).db_obj
        entity_type = self.entity_type
        step = self.step
        task = self.task
        if entity_type in ["Asset"]:
            asset_type_or_sequence = self.asset_type
            asset_or_shot = self.asset_name
        else:
            asset_type_or_sequence = self.sequence
            asset_or_shot = "%s_%s" % (self.sequence, self.shot)
        task_info = db.get_current_task(entity_type, asset_type_or_sequence, asset_or_shot, step, task)
        return task_info

    @property
    def local_work_path(self):
        return self.as_template("local", True)

    @property
    def local_image_path(self):
        return self.as_template("localImage", True)

    @property
    def local_video_path(self):
        return self.as_template("localVideo", True)

    @property
    def work_path(self):
        return self.as_template("work")

    @property
    def work_image_path(self):
        return self.as_template("workImage")

    @property
    def work_video_path(self):
        return self.as_template("workVideo")

    @property
    def other_dir(self):
        return self.as_template("other")

    @property
    def publish_path(self):
        return self.as_template("publish")

    @property
    def image_path(self):
        return self.as_template("image")

    @property
    def video_path(self):
        return self.as_template("video")

    @property
    def topology_path(self):
        return self.as_template("topology")

    @property
    def abc_cache_path(self):
        return self.as_template("cache")

    @property
    def gpu_wrap_path(self):
        return self.as_template("gpuwrap")

    @property
    def definition_path(self):
        return self.as_template("definition")

    @property
    def tex_dir(self):
        return self.as_template("tex")

    @property
    def xgen_dir(self):
        return self.as_template("xgen")

    @property
    def hair_path(self):
        return self.as_template("hair")

    @property
    def delta_path(self):
        return self.as_template("hairDelta")

    @property
    def description_path(self):
        return self.as_template("description")

    @property
    def cache_dir(self):
        return self.as_template("cache")

    @property
    def asset_info_path(self):
        return self.as_template("assetInfo")

    @property
    def shd_path(self):
        return self.as_template("shd")

    @property
    def connection_path(self):
        return self.as_template("connection")


########################################################################################################################
# below is for get asset files
########################################################################################################################
def get_task_file(project, asset_type_sequence, asset_name_shot, step, task,
                  format_str, version=None, engine="maya", local=False, edition=None):
    if local:
        primary = get_local_root_dir(project)
    else:
        primary = get_primary_dir(project)
    file_format = get_studio_value(project, format_str)
    if not file_format:
        return
    if not version:
        version_str = "000"
    else:
        version_str = version
    file_name = file_format.format(primary=primary, project=project, asset_type=asset_type_sequence,
                                   sequence=asset_type_sequence, shot=asset_name_shot.split("_")[-1],
                                   asset_name=asset_name_shot.split("_")[-1], step=step,
                                   task=task.split("_")[-1], version=version_str, edition=edition, engine=engine)
    if version is None:
        file_list = get_latest_version.get_latest_version(file_name)
        file_name = file_list[0] if file_list else file_name
    return file_name


def get_entity_dir(project, entity_type, category, asset_type_sequence, asset_name_shot):
    # "{primary}/{project}/{category}/{entity_type}/{asset_type_sequence}/{asset_name_shot}"
    entity_type = "assets" if entity_type == "Asset" else "shots"
    primary = get_studio_value(project, "primary")
    template = get_studio_value(project, "entity_dir")
    entity_dir = template.format(primary=primary, project=project, category=category, entity_type=entity_type,
                                 asset_type_sequence=asset_type_sequence,
                                 asset_name_shot=asset_name_shot.split("_")[-1])
    return entity_dir


def get_task_work_file(project, entity_type, asset_type_sequence, asset_name_shot, step, task, version=None, engine="maya", local=False):
    if entity_type == "Asset":
        format_str = "%s_asset_work" % engine
    else:
        format_str = "%s_shot_work" % engine
    work_file = get_task_file(project, asset_type_sequence, asset_name_shot, step, task, format_str, version, engine, local)
    return work_file


def get_task_workImage_file(project, entity_type, asset_type_sequence, asset_name_shot, step, task, version=None, engine="maya", local=False):
    if entity_type == "Asset":
        format_str = "%s_asset_workImage" % engine
    else:
        format_str = "%s_shot_workImage" % engine
    image_file = get_task_file(project, asset_type_sequence, asset_name_shot, step, task, format_str, version, engine, local)
    return image_file


def get_task_publish_file(project, entity_type, asset_type_sequence, asset_name_shot, step, task, version="", engine="maya", local=False):
    if entity_type == "Asset":
        format_str = "%s_asset_publish" % engine
    else:
        format_str = "%s_shot_publish" % engine
    publish_file = get_task_file(project, asset_type_sequence, asset_name_shot, step, task, format_str, version, engine, local)
    return publish_file


def get_task_video_file(project, entity_type, asset_type_sequence, asset_name_shot, step, task, version="", engine="maya", local=False):
    if entity_type == "Asset":
        format_str = "%s_asset_video" % engine
    else:
        format_str = "%s_shot_video" % engine
    publish_file = get_task_file(project, asset_type_sequence, asset_name_shot, step, task, format_str, version, engine, local)
    return publish_file


def get_asset_AD_file(project, asset_type, asset_name):
    primary = get_studio_value(project, "primary")
    template = get_studio_value(project, "maya_asset_definition")
    ad_file = template.format(primary=primary, project=project, asset_type=asset_type, asset_name=asset_name)
    return ad_file


########################################################################################################################
# below is for get shot files
########################################################################################################################
if __name__ == "__main__":
    print get_task_publish_file("SnowKidTest", "Asset", "Prop", "TdTest", "HighMdl", "HighMdl")