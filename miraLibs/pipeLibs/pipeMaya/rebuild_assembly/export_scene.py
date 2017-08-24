import maya.cmds as mc
import pymel.core as pm
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import Assembly


BASE_ATTRIBUTES = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']


def export_scene(ar_node, yml_path):
    # switch to mid rig

    # record ar_node name, def name and namespace and rep
    #
    def_name = mc.getAttr("%s.def" % ar_node)
    name_space = mc.getAttr("%s.rns" % ar_node)




