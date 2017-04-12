# -*- coding: utf-8 -*-
import maya.cmds as mc


class ReferenceUtility(object):

    def get_all_ref(self):
        all_ref = mc.ls(type='reference')
        all_ref = [ref for ref in all_ref if 'sharedReferenceNode' not in ref]
        return all_ref

    def get_ref_by_obj(self, selected_objects=None):
        if not selected_objects:
            selected_objects = mc.ls(sl=1)
        if selected_objects:
            ref_node_names = [mc.referenceQuery(obj, referenceNode=1, topReference=1)
                              for obj in selected_objects
                              if mc.referenceQuery(obj, isNodeReferenced=1)]
            ref_node_names = list(set(ref_node_names))
            # if not mc.window('referenceEditorPanel1Window', ex=1):
            #     mc.ReferenceEditor()
            # ref_panel = mel.eval("$gReferenceEditorPanel = $gReferenceEditorPanel")
            # all_ref = self.get_all_ref()
            # for index, ref in enumerate(all_ref):
            #     mc.sceneEditor(ref_panel, e=1, si=index)
            #     sel_ref = mc.sceneEditor(ref_panel, q=1, selectReference=1)
            #     if sel_ref[0] == ref_node_names[0]:
            #         break
            return ref_node_names
        else:
            print '[OF] info: Nothing Selected!'

    def get_obj_by_ref(self, ref_nodes):
        all_transforms = list()
        for ref_node in ref_nodes:
            child_ref_nodes = self.get_child_ref(ref_node)
            if child_ref_nodes:
                for child in child_ref_nodes:
                    all_objs = mc.referenceQuery(child, dagPath=1, nodes=1)
                    transforms = mc.ls(all_objs, type='transform')
                    all_transforms.extend(transforms)
            else:
                all_objs = mc.referenceQuery(ref_node, dagPath=1, nodes=1)
                transforms = mc.ls(all_objs, type='transform')
                all_transforms.extend(transforms)
        if all_transforms:
            all_transforms = list(set(all_transforms))
            mc.select(all_transforms, r=1)

    def remove_ref(self, ref_node):
        parent_ref = self.get_parent_ref(ref_node)
        if not parent_ref:
            file_name = self.get_file_name(ref_node)
            mc.file(file_name, rr=1)
        else:
            parent_file_name = self.get_file_name(parent_ref)
            mc.file(parent_file_name, rr=1)

    def remove_unload_ref(self):
        all_ref = mc.file(q=1, r=1)
        if all_ref:
            for ref in all_ref:
                a = mc.referenceQuery(ref, isLoaded=1)
                if not a:
                    mc.file(ref, removeReference=1)

    def import_loaded_ref(self):
        while 1:
            all_ref = mc.file(q=1, r=1)
            if all_ref:
                for ref in all_ref:
                    a = self.check_loaded(ref)
                    if a:
                        mc.file(ref, importReference=1)
            else:
                break

    def check_loaded(self, ref_node):
        result = mc.referenceQuery(ref_node, isLoaded=1)
        return result

    def get_file_name(self, ref_node):
        file_name = mc.referenceQuery(ref_node, filename=1)
        return file_name

    def get_all_ref_list(self):
        all_ref = self.get_all_ref()
        all_ref_list = [[ref, self.get_file_name(ref)] for ref in all_ref]
        return all_ref_list

    def get_all_top_reference(self):
        all_top_ref_file = mc.file(q=1, r=1)
        all_top_ref_node = [mc.referenceQuery(ref, referenceNode=1) for ref in all_top_ref_file]
        return all_top_ref_node

    def get_child_ref(self, ref_node):
        return mc.referenceQuery(ref_node, child=1, referenceNode=1)

    def get_parent_ref(self, ref_node):
        return mc.referenceQuery(ref_node, parent=1, referenceNode=1)

    def import_reference(self, ref_node):
        file_name = self.get_file_name(ref_node)
        mc.file(file_name, importReference=1)

    def load_reference(self, ref_node):
        mc.file(loadReference=ref_node)

    def unload_reference(self, ref_node):
        mc.file(unloadReference=ref_node)

    def remove_all_ref(self):
        all_ref_nodes = self.get_all_ref()
        for ref_node in all_ref_nodes:
            try:
                self.remove_ref(ref_node)
            except:pass

    def load_all_unloaded_ref(self):
        all_ref_nodes = self.get_all_ref()
        for ref_node in all_ref_nodes:
            if not self.check_loaded(ref_node):
                self.load_reference(ref_node)


if __name__ == "__main__":
    pass
