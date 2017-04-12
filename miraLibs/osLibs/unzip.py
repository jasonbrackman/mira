# -*- coding: utf-8 -*-
import zipfile


def unzip(zip_file, target_path="D:/"):
    f = zipfile.ZipFile(zip_file, 'r')  
    for file_name in f.namelist():
        f.extract(file_name, target_path)
