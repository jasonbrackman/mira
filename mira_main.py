# -*- coding: utf-8 -*-
import os
import logging
import getpass
import shutil
import xml.dom.minidom
import maya.cmds as mc
import maya.mel as mel
import maya.utils as mu
import miraCore
from miraLibs.mayaLibs import set_image_size, get_maya_version


logger = logging.getLogger(u"MIRA MAIN")
logger.setLevel(logging.DEBUG)

conf_dir = miraCore.conf_dir

# ------------------------------------------------------------------------------------------#
# ----------------------------------load menu  ---------------------------------------------#
# ------------------------------------------------------------------------------------------#


def get_menu_conf_path():
    menu_conf_path = os.path.join(conf_dir, "mayaMenu.xml")
    return menu_conf_path


def run_mel_cmd(mel_path):
    mel.eval("source \"%s\"" % mel_path)


def load_menu():
    try:
        mc.delteUI("[MIRA]")
    except:
        pass
    menu_conf_path = get_menu_conf_path()
    dom_tree = xml.dom.minidom.parse(menu_conf_path)
    collection = dom_tree.documentElement
    maya_version = get_maya_version.get_maya_version()
    main_maya_menu = mc.menu('test', label=collection.getAttribute("name"), tearOff=True,
                             parent='MayaWindow', version=maya_version)

    sub_menus = collection.getElementsByTagName("submenu")
    for sub_menu in sub_menus:
        name = sub_menu.getAttribute("name")
        menu_type = sub_menu.getAttribute("type")
        if menu_type == "submenu":
            sub_maya_menu = mc.menuItem(sm=1, label=name, tearOff=True, parent=main_maya_menu)
            cmd_menues = sub_menu.getElementsByTagName("command")
            for cmd_menu in cmd_menues:
                cmd_menu_name = cmd_menu.getAttribute("name")
                cmd = cmd_menu.getAttribute("cmd")
                mode = cmd_menu.getAttribute("mode")
                if mode == "python":
                    mc.menuItem(label=cmd_menu_name, tearOff=True, parent=sub_maya_menu, c=cmd)
                elif mode == "mel":
                    mel_path = os.path.join(miraCore.mira_dir, cmd)
                    mel_path = mel_path.replace("\\", "/")
                    mc.menuItem(label=cmd_menu_name, tearOff=True, parent=sub_maya_menu,
                                c=lambda *args: run_mel_cmd(mel_path))

        elif menu_type == "command":
            mc.menuItem(label=name, tearOff=True, parent=main_maya_menu, c=sub_menu.getAttribute('cmd'))

        elif menu_type == "separator":
            mc.menuItem(parent=main_maya_menu, divider=1)
    logger.debug("Load menu done")


# ------------------------------------------------------------------------------------------#
# ----------------------------------reload shelves -----------------------------------------#
# ------------------------------------------------------------------------------------------#


def reload_shelves():
    from miraPipeline.maya.shelf import reload_shelves
    reload_shelves.main()
    logger.info("Reload shelves done.")

# ------------------------------------------------------------------------------------------#
# ----------------------------------init user setup-----------------------------------------#
# ------------------------------------------------------------------------------------------#


def init_user_setup():
    init_maya_background_style()
    init_maya_saver_timer()
    # close_panel_when_open_and_save()
    init_wireframe_when_open()
    init_current_project()
    load_plugins()
    init_render_setting()
    init_scene_break_down()
    add_system_python_path_env()
    # init_shotgun()
    open_port()
    # remove_invalid_clipboard_data()


def init_maya_saver_timer():
    from miraPipeline.maya.maya_save_timer import maya_save_timer
    maya_save_timer.maya_save_timer()
    logger.info("Initialize maya save timer done.")


def init_scene_break_down():
    from miraPipeline.maya.scene_break_down import auto_tip_update
    auto_tip_update.auto_tip_update()
    logger.info("Initialize scene break down done.")


def init_render_setting():
    from miraLibs.pipeLibs import pipeMira
    current_project = pipeMira.get_current_project()
    resolution = pipeMira.get_resolution(current_project)
    set_image_size.set_image_size(*resolution)
    logger.info("Initialize render settings done.")


def close_panel_when_open_and_save():
    from miraLibs.mayaLibs import close_panel_open_and_save
    close_panel_open_and_save.close_panel_open_and_save()
    logger.info("Initialize close panel done.")


def remove_invalid_clipboard_data():
    from miraLibs.mayaLibs import remove_invalid_clipboard_data
    remove_invalid_clipboard_data.remove_invalid_clipboard_data()
    logger.info("Can copy from PyCharm to maya done")


def init_wireframe_when_open():
    from miraLibs.mayaLibs import display_wireframe
    import maya.OpenMaya as OpenMaya
    OpenMaya.MEventMessage.addEventCallback("SceneOpened", display_wireframe.display_wireframe)
    logger.info("Initialize when open file wireframe display done.")


def init_maya_background_style():
    mc.displayPref(displayGradient=1)
    logger.info("Initialize maya background style done.")


def load_plugins():
    from miraLibs.pipeLibs.pipeMaya import load_plugins, unload_plugins
    load_plugins.load_plugins()
    unload_plugins.unload_plugins()


def init_current_project():
    from miraPipeline.maya.switch_project import switch_project
    switch_project.main()
    logger.info("Initialize current project done.")


def open_port():
    import subprocess
    from miraPipeline.pipeline.port_operation import add_user_info_to_db
    add_user_info_to_db.add_user_info_to_db()
    open_port_path = os.path.join(miraCore.mira_dir, "miraPipeline/pipeline/port_operation/run_open_port.py")
    open_port_path = open_port_path.replace("\\", "/")
    if not os.path.isfile(open_port_path):
        return
    os.popen("tskill pythonw")
    python_path = "C:/Python27/pythonw"
    command = "%s %s" % (python_path, open_port_path)
    subprocess.Popen(command)
    user = getpass.getuser()
    startup_dir = "C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup" % user
    startup_path = "%s/%s" % (startup_dir, "mira.bat")
    if os.path.isfile(startup_path):
        os.remove(startup_path)
    with open(startup_path, "w") as f:
        f.write("start %s" % command)
    logger.info("Initialize open port done.")


def add_system_python_path_env():
    user = getpass.getuser()
    if user in ["heshuai", "zhaopeng"]:
        return
    startup_dir = "C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup" % user
    mira_batch_dir = miraCore.batch_dir
    python_path_bat = os.path.join(mira_batch_dir, "PYTHONPATH.bat").replace("\\", "/")
    startup_python_path_bat = os.path.join(startup_dir, "PYTHONPATH.bat")
    try:
        os.system(python_path_bat)
        shutil.copyfile(python_path_bat, startup_python_path_bat)
        logger.info("add system python path env done.")
    except:
        logger.info("add system python path env failed.")


def init_shotgun():
    from miraPipeline.maya.init_shotgun import init_shotgun
    init_shotgun.main()
    logger.info("Initialize shotgun done.")


# ------------------------------------------------------------------------------------------#
# -------------------------------------main-------------------------------------------------#
# ------------------------------------------------------------------------------------------#


def main():
    mu.executeDeferred("import mira_main;mira_main.load_menu()")
    mu.executeDeferred("import mira_main;mira_main.init_user_setup()")
    mu.executeDeferred("import mira_main;mira_main.reload_shelves()")


if __name__ == "__main__":
    main()
