import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile


class Check(BaseCheck):

    def run(self):
        context = pipeFile.PathDetails.parse_path()
        sequence = context.sequence
        set_node = "%s_c000_set" % sequence
        if mc.objExists(set_node):
            self.pass_check("%s exist" % set_node)
        else:
            self.fail_check("%s does not exist." % set_node)
