# -*- coding: utf-8 -*-
import getpass
import os
import shutil
import logging
from distutils.dir_util import copy_tree


logger = logging.getLogger(__name__)


def copytree(src, dst):
    copy_tree(src, dst)


def copy_plugins():
    server_plugin_dir = "Z:/tools"
    local_plugin_dir = "C:/tools"
    # stop redshift service
    try:
        os.system("sc delete RLM-Redshift")
    except:pass
    if os.path.isdir(local_plugin_dir):
        try:
            os.rmdir(local_plugin_dir)
        except:
            shutil.rmtree(local_plugin_dir)
    dir_name = os.path.dirname(local_plugin_dir)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    copytree(server_plugin_dir, local_plugin_dir)


def add_env_variable():
    user = getpass.getuser()
    if user in ["heshuai", "zhaopeng"]:
        return
    startup_dir = "C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup" % user
    mira_batch_dir = "Z:/mira/miraBatch"
    python_path_bat = os.path.join(mira_batch_dir, "PYTHONPATH.bat").replace("\\", "/")
    startup_python_path_bat = os.path.join(startup_dir, "PYTHONPATH.bat")
    try:
        os.system(python_path_bat)
        shutil.copyfile(python_path_bat, startup_python_path_bat)
        logger.info("add system python path env done.")
    except:
        logger.info("add system python path env failed.")


def copy_maya_env():
    server_env_path = "Z:/mira/Maya.env"
    local_maya_dir = os.path.join(os.environ["USERPROFILE"], "Documents", "maya").replace("\\", "/")
    for i in os.listdir(local_maya_dir):
        if i.startswith("20"):
            version_dir = os.path.join(local_maya_dir, i).replace("\\", "/")
            maya_env_path = os.path.join(version_dir, "Maya.env")
            shutil.copyfile(server_env_path, maya_env_path)


def copy_nuke_env():
    local_nuke_env_dir = os.path.join(os.environ["USERPROFILE"], ".nuke").replace("\\", "/")
    if not os.path.isdir(local_nuke_env_dir):
        print "%s is not an exist dir." % local_nuke_env_dir
        return
    local_nuke_env_path = "%s/%s" % (local_nuke_env_dir, "menu.py")
    if not os.path.isfile(local_nuke_env_path):
        f = open(local_nuke_env_path, 'w')
        f.close()
    with open(local_nuke_env_path, "a") as f:
        f.write('nuke.pluginAddPath("Z:/mira/miraEnv/nuke")')


def main():
    add_env_variable()
    print "Add environment variable done."
    copy_maya_env()
    print "Copy  maya env done."
    copy_nuke_env()
    print "Copy nuke env done."
    # print "Plugins Copying......."
    # copy_plugins()
    # print "Copy plugins done."


if __name__ == "__main__":
    main()

