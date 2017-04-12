# -*- coding: utf-8 -*-
import os


def walk_path(directory):
    dir_dict = dict()
    folders = dict()
    files = list()
    for file in os.listdir(directory):
        full_file_path = os.path.abspath(os.path.join(directory, file))
        if os.path.isdir(full_file_path):
            folders[file] = walk_path(full_file_path)
        else:
            files.append(file)
    dir_dict["folders"] = folders
    dir_dict["files"] = files
    return dir_dict


if __name__ == "__main__":
    pass
