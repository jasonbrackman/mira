# -*- coding: utf-8 -*-
import os


mira_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
mira_dir = mira_dir.replace("\\", "/")


def get_package_dir(package_name):
    package_dir = os.path.abspath(os.path.join(mira_dir, package_name))
    package_dir = package_dir.replace("\\", "/")
    return package_dir


app_dir = get_package_dir("miraApp")
conf_dir = get_package_dir("miraConf")
data_dir = get_package_dir("miraData")
framework_dir = get_package_dir("miraFramework")
history_dir = get_package_dir("miraHistory")
icons_dir = get_package_dir("miraIcons")
libs_dir = get_package_dir("miraLibs")
scripts_dir = get_package_dir("miraScripts")
bin_dir = get_package_dir("miraBin")
batch_dir = get_package_dir("miraBatch")
pipeline_dir = get_package_dir("miraPipeline")
