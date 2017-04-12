# -*- coding: utf-8 -*-
import sys
from get_parent_dir import get_parent_dir


parent_dir = get_parent_dir()
parent_dir = parent_dir.replace('\\', '/')
print parent_dir
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


if __name__ == "__main__":
    pass
