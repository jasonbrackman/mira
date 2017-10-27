# -*- coding: utf-8 -*-
import glob
import logging
import os
import sys

import maya.cmds as mc

logger = logging.getLogger("userSetup.py")


def add_to_python_path(python_path):
    python_path = python_path.replace("\\", "/")
    if python_path not in sys.path:
        sys.path.append(python_path)
    logger.info("Add %s to maya PYTHONPATH" % python_path)


def get_python_version():
    return "py%s" % sys.version[:3].replace(".", "")


def set_maya_env():
    module_name = "miraEnv"
    module_path = mc.getModulePath(moduleName=module_name)
    mira_dir = module_path.split(module_name)[0]
    # add mira to PYTHONPATH
    add_to_python_path(mira_dir)
    # add python path
    miraLibs_dir = os.path.join(mira_dir, "miraLibs")
    site_packages_dir = os.path.join(miraLibs_dir, "site-packages")
    add_to_python_path(site_packages_dir)
    # add current python packages to PYTHONPATH
    python_version = get_python_version()
    current_python_dir = os.path.join(site_packages_dir, python_version)
    add_to_python_path(current_python_dir)
    # add .egg files to PYTHONPATH
    egg_files = glob.glob("%s/*.egg" % site_packages_dir)
    if egg_files:
        for egg_file in egg_files:
            add_to_python_path(egg_file)


def run_mira_main():
    import mira_main
    reload(mira_main)
    mira_main.main()
    logger.info("Run >>>>mira_main.main()<<<<")


if __name__ == "__main__":
    set_maya_env()
    run_mira_main()
