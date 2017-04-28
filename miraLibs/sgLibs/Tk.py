# -*- coding: utf-8 -*-
import os
from get_tk_object import get_tk_object


class Tk(object):
    def __init__(self, project):
        self.project = project
        self.tk = get_tk_object(self.project)
        self.sg = self.tk.shotgun

    def get_context_from_path(self, path):
        context = self.tk.context_from_path(path)
        return context

    def get_task_from_path(self, path):
        context = self.get_context_from_path(path)
        return context.task

    def publish_file(self, publish_file_path, status="cmpt", file_type_name="Maya Scene", description="", user=None):
        from miraLibs.pyLibs import get_version_number
        import sgtk
        version_number = get_version_number.get_version_number(publish_file_path)
        args = {
            "tk": self.tk,
            "context": self.tk.context_from_path(publish_file_path),
            "path": publish_file_path,
            "name": os.path.basename(publish_file_path),
            "version_number": version_number,
            "comment": description,
            "published_file_type": file_type_name,
            "sg_fields": {"sg_status_list": status}
        }
        if user:
            args["created_by"] = user
        new_publish = sgtk.util.register_publish(**args)
        return new_publish
