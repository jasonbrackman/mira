# -*- coding: utf-8 -*-
import os


mira_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_package_dir(package_name):
    package_dir = os.path.abspath(os.path.join(mira_dir, package_name))
    return package_dir


def get_app_dir():
    return get_package_dir("miraApp")


def get_conf_dir():
    return get_package_dir("miraConf")


def get_data_dir():
    return get_package_dir("miraData")


def get_framework_dir():
    return get_package_dir("miraFramework")


def get_history_dir():
    return get_package_dir("miraHistory")


def get_icons_dir():
    return get_package_dir("miraIcons")


def get_libs_dir():
    return get_package_dir("miraLibs")


def get_scripts_dir():
    return get_package_dir("miraScripts")


def get_bin_dir():
    return get_package_dir("miraBin")


def get_batch_dir():
    return get_package_dir("miraBatch")


def get_pipeline_dir():
    return get_package_dir("miraPipeline")
