#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/11/23'
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import sys

# -Append tank to syspath so we can import it
core_path = os.path.abspath(r"Z:\Resource\Pipeline\app_config\sgtk\tank\install\core\python")
sys.path.append(core_path)

# Third-party modules
import tank             #from tank.util.shotgun import Sh
import sgtk

# Studio modules

# Local modules


def get_tk_object(api_script="tank", 
                  api_key="f28b2d9918667f240426d33d3ce3ad4c9d589c9ccba6cc3db6c59aaa28403fb8", 
                  root_pn=r"Z:\Resource\Pipeline\app_config\settings\projects\df\sgtk\main"):
    # connect to shotgun server
    tk_connect(api_script, api_key)
    # init a tk object
    return tank.tank_from_path(root_pn)
    
    
def tk_connect(api_script, api_key):
    # Import Toolkit so we can access to Toolkit specific features.
    # Import the ShotgunAuthenticator from the tank_vendor.shotgun_authentication
    # module. This class allows you to authenticate either interactively or, in this
    # case, programmatically.
    from tank_vendor.shotgun_authentication import ShotgunAuthenticator

    # Instantiate the CoreDefaultsManager. This allows the ShotgunAuthenticator to
    # retrieve the site, proxy and optional script_user credentials from shotgun.yml
    cdm = sgtk.util.CoreDefaultsManager()

    # Instantiate the authenticator object, passing in the defaults manager.
    authenticator = ShotgunAuthenticator(cdm)

    # Create a user programmatically using the script"s key.
    user = authenticator.create_script_user(api_script, api_key)
    # print "User is "%s"" % user
    # Tells Toolkit which user to use for connecting to Shotgun.
    sgtk.set_authenticated_user(user)
