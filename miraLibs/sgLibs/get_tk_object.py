# -*- coding: utf-8 -*-
import sys
from shotgunConfParser import ShotgunConfParser

core_path = ShotgunConfParser.sg_conf_data().get("tank_path")
if core_path not in sys.path:
    sys.path.append(core_path)
import tank
import sgtk


def get_tk_object(project):
    conf_data = ShotgunConfParser.sg_conf_data()
    api_script = conf_data.get("script_name")
    api_key = conf_data.get("api_key")
    root_pn = conf_data[project].get("root_pn")
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


def tk_connect_bak(api_script, api_key, host):
    """
    :param api_script: shotgun script name
    :param api_key: key
    :param host: host url
    :return:
    """
    sa = sgtk.authentication.ShotgunAuthenticator()

    # Use the authenticator to create a user object. This object
    # identifies a Shotgun user or script and also wraps around
    # a Shotgun API instance which is associated with that user.
    user = sa.create_script_user(api_script=api_script,
                                 api_key=api_key,
                                 host=host)

    # tell the Toolkit Core API which user to use
    sgtk.set_authenticated_user(user)
