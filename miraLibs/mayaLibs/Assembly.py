# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
logger = logging.getLogger("Assembly")


class Assembly(object):

    def __init__(self):
        pass

    @staticmethod
    def create_assembly_node(name, typ):
        if typ not in ["assemblyDefinition", "assemblyReference"]:
            logger.error("type is wrong")
            return
        assembly_node = mc.assembly(name=name, type=typ)
        return assembly_node

    @staticmethod
    def get_representation_index(node, rep_name):
        all_representation = mc.assembly(node, q=1, listRepresentations=1)
        if rep_name in all_representation:
            return all_representation.index(rep_name)

    @staticmethod
    def create_representation(node, rep_type, rep_name, rep_label, input_path):
        if not mc.objExists(node):
            logger.error("%s does not exist." % node)
            return
        all_representation = mc.assembly(node, q=1, listRepresentations=1)
        if all_representation and rep_name in all_representation:
            logger.warning("%s in the representation" % rep_name)
            return
        mc.assembly(node, e=1, createRepresentation=rep_type, repName=rep_name, input=input_path)
        all_representation = mc.assembly(node, q=1, listRepresentations=1)
        index = all_representation.index(rep_name)
        if rep_label:
            mc.setAttr("%s.rep[%s].rla" % (node, index), rep_label, type="string")

    def reference_ad(self, name, ad_path):
        ar_node = self.create_assembly_node(name, "assemblyReference")
        mc.setAttr("%s.definition" % ar_node, ad_path, type="string")
        return ar_node
