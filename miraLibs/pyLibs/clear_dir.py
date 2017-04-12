# -*- coding: utf-8 -*-
import os


def clear_dir(directory):
    for child in os.listdir(directory):
        child_full_path = os.path.abspath(os.path.join(directory, child))
        if os.path.isdir(child_full_path):
            os.rmdir(child_full_path)
        else:
            os.remove(child_full_path)


if __name__ == "__main__":
    pass
