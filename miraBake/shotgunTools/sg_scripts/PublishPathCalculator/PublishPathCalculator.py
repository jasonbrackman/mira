# Created on Oct 26, 2012
# @author: patrick.wolf
# the associated config file from tank is here ...
# "\\work\app_config\release\tank_config\xxtank-test5_xt5-0000\tank\config\core\templates.yml"

import os
import sys
# Append tank to syspath so we can import it
core_path = os.path.abspath(r"D:\mnt\shotgun\studio\install\core\python")
sys.path.append(core_path)

#import unittest
from pprint import pprint
#from tank.util.shotgun import Sh
import tank
import sgtk

# project_id = 68


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


def get_tk_object(api_script, api_key, root_pn):
    # connect to shotgun server
    tk_connect(api_script, api_key)
    # init a tk object
    return tank.tank_from_path(root_pn)
    
    
def get_task_type_engine(task_type):
    if task_type == "art":
        return "photoshop"
    return "maya"
        

class PublishPathCalculator(object):
    
    def __init__(self, 
                 api_script="hsToolkit", 
                 api_key="2076a098b4e0e644762a2162a93cd6b6b9461ad102e1ac17b314089b032f4c79", 
                 root_pn=r"D:\mnt\shotgun\pipeline\hsTest"):
        self.tk = get_tk_object(api_script, api_key, root_pn)
        self.sg = self.tk.shotgun

    def _get_asset_task_id(self, asset_name, task_type):
        filters = [["entity","name_is",asset_name],["sg_task_type", "name_is", task_type]]
        task_id  = self.sg.find_one("Task",filters)["id"]
        return task_id
        
    def _calculat_file_path(self, task_id, engine):
        template = self.tk.templates["%s_asset_publish" % engine]
        # create folders for this asset
        #print self.tk.preview_filesystem_structure("Task", task_id)[5]
        self.tk.create_filesystem_structure("Task", task_id, engine="tk-%s" % engine)
        ctx = self.tk.context_from_entity("Task", task_id)
        fields = ctx.as_template_fields(template)
        fields["version"] = 0
        return template.apply_fields(fields)
    
    def calculat(self, asset_name, task_type):
        task_id = self._get_asset_task_id(asset_name, task_type)
        engine = get_task_type_engine(task_type)
        return self._calculat_file_path(task_id, engine)

if __name__ == "__main__":
    path_calculator = PublishPathCalculator()
    print path_calculator.calculat("Nurse", "mdl")
