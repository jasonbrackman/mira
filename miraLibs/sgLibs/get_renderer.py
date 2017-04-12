# -*- coding: utf-8 -*-
from get_standalone_sg import get_standalone_sg


def get_renderer(project_name):
    sg = get_standalone_sg()
    project = sg.find_one("Project", [["name", "is", project_name]], ["sg_renderer"])
    if project:
        renderer = project['sg_renderer']
        return renderer

if __name__ == "__main__":
    pass
