# -*- coding: utf-8 -*-
from miraLibs.pipeLibs.pipeMaya import get_current_project
from miraLibs.pipeLibs import pipeMira


class UploadFile:
    def __init__(self):
        self.current_project = get_current_project.get_current_project()
        self.current_root = pipeMira.get_root_dir(self.current_project)

    def upload(self):
        pass




if __name__ == '__main__':
    pass