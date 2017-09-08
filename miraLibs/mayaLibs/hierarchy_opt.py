# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
import json


class HierarchyOpt(object):
    def __init__(self, group=None):
        self.group = group

    def shapes(self):
        all_shape = mc.listRelatives(self.group, ad=1, f=1, type="mesh")
        return all_shape

    def transforms(self):
        shapes = self.shapes()
        transforms = [mc.listRelatives(shape, f=1, parent=1)[0] for shape in shapes]
        transforms = list(set(transforms))
        return transforms

    def get_topology(self):
        topology_dict = dict()
        transforms = self.transforms()
        for transform in transforms:
            vertex_num = mc.polyEvaluate(transform, v=1)
            edge_num = mc.polyEvaluate(transform, e=1)
            face_num = mc.polyEvaluate(transform, f=1)
            topology_dict[transform] = dict(vertex=vertex_num, edge=edge_num, face=face_num)
        return topology_dict

    def write_out(self, json_file):
        json_dir = os.path.dirname(json_file)
        if not os.path.isdir(json_dir):
            os.makedirs(json_dir)
        topology = self.get_topology()
        with open(json_file, "w") as f:
            json.dump(topology, f)

    @staticmethod
    def read(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)

    def compare_hierarchy(self, json_file):
        old_dict = self.read(json_file)
        new_dict = self.get_topology()
        if old_dict == new_dict:
            return [], []
        old_hierarchy_list = old_dict.keys()
        new_hierarchy_list = new_dict.keys()
        new_hierarchy_list = ["|".join(("", self.group, obj.split("%s|" % self.group)[1])) for obj in new_hierarchy_list]
        decrease_list = list(set(new_hierarchy_list)-set(old_hierarchy_list))
        increase_list = list(set(old_hierarchy_list)-set(new_hierarchy_list))
        return increase_list, decrease_list

    def compare_topology(self, json_file):
        changed_list = list()
        old_dict = self.read(json_file)
        new_dict = self.get_topology()
        temp_dict = dict()
        for key in new_dict:
            new_name = "|".join(("", self.group, key.split("%s|" % self.group)[1]))
            temp_dict[new_name] = new_dict[key]
        if old_dict == temp_dict:
            return []
        for key in temp_dict:
            if old_dict[key] != temp_dict[key]:
                changed_list.append(key)
        return changed_list
