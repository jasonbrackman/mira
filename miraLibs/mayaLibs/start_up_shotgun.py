#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_libs_start_up_shotgun
# description : ''
# author      : Aaron Hui
# date        : 2015/12/16
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import sys
import logging

# add a custom python path
sys.path.append(r"Z:\Resource\Pipeline\app_config\settings\projects\df\sgtk\dev\install\core\python")

# Third-party modules

# Studio modules
import tank
import tank_vendor
import pymel.core as pm

import libs.sgLibs as sg_lib
import libs.osLibs as os_lib


# constants
engine_name = "tk-maya"


def start_up_shotgun(project_name="df"):

    # get tk
    tk = sg_lib.get_tk_object()
    # get path
    os_type = os_lib.get_os_type()
    if os_type == "osx":
        os_type = "mac"
    storage = tk.shotgun.find_one("LocalStorage",[["code", "is", "primary"]], ["%s_path" % os_type])
    storage_path = storage["%s_path" % os_type]
    if not storage_path:
        return
    project_path = os.path.join(storage_path, project_name)

    # get current user
    sg_login = os_lib.get_shotgun_login()
    current_user = tk.shotgun.find_one("HumanUser", [["login", "is", sg_login]], ["login"])

    # login authentication
    impl = tank_vendor.shotgun_authentication.user_impl.SessionUser(host=r"http://shotgun.antsanimation.com",
                                                                    login=current_user["login"],
                                                                    session_token=None,
                                                                    http_proxy=None)
    user = tank_vendor.shotgun_authentication.user.ShotgunUser(impl)
    tank.api.set_authenticated_user(user)
    # tank.util.get_current_user(tk)

    # clear old engine
    if tank.platform.current_engine():
        tank.platform.current_engine().destroy()
    if pm.menu("ShotgunMenu", exists=True):
        pm.deleteUI("ShotgunMenu")
    if pm.menu("ShotgunMenuDisabled", exists=True):
        pm.deleteUI("ShotgunMenuDisabled")

    # start up new engine
    context = tk.context_from_path(project_path)
    user_context = context.create_copy_for_user(current_user)
    tank.platform.engine.start_engine(engine_name, user_context.tank, user_context)


if __name__ == "__main__":
    start_up_shotgun()
