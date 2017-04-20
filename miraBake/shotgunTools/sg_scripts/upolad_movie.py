#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/11/23'
# version     :
# usage       :
# notes       :
import os
import urllib

# local modules
import add_environ
from sg_utils.get_tk_object import get_tk_object


def download_image(image_url):
    if not os.environ. has_key('tmp'):
        raise Exception("has no tmp key in os.environ")
    temp_dir = os.path.join(os.environ['tmp'], 'temp.png')
    temp_dir = temp_dir.replace('\\', '/')
    data = urllib.urlopen(image_url).read()  
    with open(temp_dir, 'wb') as f:
        f.write(data)
    return os.path.abspath(temp_dir)
        

def upload_movie():
    tk = get_tk_object()
    sg = tk.shotgun
    versions = sg.find('Version', [], [])
    num_versions = len(versions)
    for version in versions:
        print "%s left" % num_versions
        version_info = sg.find_one('Version', [['id', 'is', version['id']]], ['code', 'image', 'sg_uploaded_movie'])
        num_versions -= 1
        if version_info['sg_uploaded_movie']:
            continue
        if not version_info['image']:
            continue
        image_url = version['image']
        image_path = download_image(image_url)
        sg.upload('Version', version['id'], image_path, 'sg_uploaded_movie')
        

if __name__ == '__main__':
    upload_movie()
