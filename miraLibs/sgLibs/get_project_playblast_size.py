# -*- coding: utf-8 -*-
from get_standalone_sg import get_standalone_sg


def get_project_playblast_size(project_name):
    sg = get_standalone_sg()
    project = sg.find_one("Project", [["name", "is", project_name]], ["sg_resolutionplayblast"])
    if project:
        if project["sg_resolutionplayblast"]:
            size = project["sg_resolutionplayblast"].split("x")
            size = [int(i) for i in size]
            return size
        return [1920, 1080]


if __name__ == "__main__":
    pass
