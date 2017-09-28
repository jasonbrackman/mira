# -*- coding: utf-8 -*-
import os
import miraCore
import logging
import miraLibs.pyLibs.yml_operation as yml
import miraLibs.pyLibs.join_path as join_path


conf_dir = miraCore.get_conf_dir()


# ******************************get studio value****************************** #
def get_value(project_name, name, option):
    conf_path = join_path.join_path2(conf_dir, project_name, "%s.yml" % name)
    if os.path.isfile(conf_path):
        dcp = yml.DeepConfParser(conf_path)
        yml_data = dcp.parse()
        if yml_data. has_key(option):
            value = yml_data[option]
            return value
        else:
            logging.error("pipeMira: KeyError")
    else:
        logging.error("pipeMira: %s not in the config file: %s" % (project_name, conf_path))


def get_studio_value(project_name, option):
    studio_value = get_value(project_name, "studio", option)
    return studio_value


def get_step_value(project_name, step):
    step_value = get_value(project_name, "step", step)
    return step_value


def get_root_dir(project_name):
    root_dir = get_studio_value(project_name, "root_dir")
    return root_dir


def get_vfx_cache_root_dir(project_name):
    vfx_cache_dir = get_studio_value(project_name, "vfx_cache_root_dir")
    return vfx_cache_dir


def get_local_root_dir(project_name):
    local_root_dir = get_studio_value(project_name, "local_root_dir")
    return local_root_dir


def get_resolution(project_name):
    resolution_str = get_studio_value(project_name, "resolution")
    resolution = resolution_str.split("*")
    resolution = [int(value) for value in resolution]
    return resolution


def get_maya_path(project_name):
    maya_path = get_studio_value(project_name, "maya_path")
    return maya_path


def get_mayabatch_path(project_name):
    mayabatch_path = get_studio_value(project_name, "mayabatch_path")
    return mayabatch_path


def get_playblast_percent(project_name):
    percent = get_studio_value(project_name, "playblast_percent")
    return percent


def get_primary_dir(project_name):
    primary_dir = get_studio_value(project_name, "primary")
    return primary_dir


# ******************************get project value****************************** #


def get_project_value():
    project_conf_dir = join_path.join_path2(conf_dir, "projects.yml")
    yml_data = yml.get_yaml_data(project_conf_dir)
    return yml_data


def get_projects():
    project_value = get_project_value()
    projects_str = project_value["projects"]
    projects = projects_str.split(",")
    projects = [project for project in projects if project]
    return projects


def get_current_project():
    project_value = get_project_value()
    current_project = project_value["current_project"]
    return current_project


# ******************************get asset type value****************************** #
def get_company():
    company_conf_path = join_path.join_path2(conf_dir, "company.yml")
    yml_data = yml.get_yaml_data(company_conf_path)
    return yml_data["company"]


# ******************************get load plugins value****************************** #
def get_load_plugins():
    plugin_conf_path = join_path.join_path2(conf_dir, "plugins.yml")
    yml_data = yml.get_yaml_data(plugin_conf_path)
    load_plugins = yml_data["plugins"]["load"]
    return load_plugins


def get_unload_plugins():
    plugin_conf_path = join_path.join_path2(conf_dir, "plugins.yml")
    yml_data = yml.get_yaml_data(plugin_conf_path)
    unload_plugins = yml_data["plugins"]["unload"]
    return unload_plugins


if __name__ == "__main__":
    pass
