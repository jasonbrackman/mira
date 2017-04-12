#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_utility
# description : ''
# author      : HeShuai
# date        : 2016/1/12
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import re
import shutil
import cStringIO
import sys
# Third-party modules

# Studio modules

# Local modules


logging.basicConfig(
    filename=os.path.join(os.environ["TMP"], 'aas_repos_utility_log.txt'),
    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


if sys.platform.startswith('win'):
    os_type = 'win'
elif sys.platform.startswith('linux'):
    os_type = 'linux'
else:
    os_type = 'mac'


def get_maya_version(scene_name):
    ext = os.path.splitext(scene_name)[1].lower()
    f = open(scene_name, 'r')
    line = f.readline()
    if ext == '.ma':
        version = re.findall(r'//Maya ASCII (\d+) scene', line, re.I)
        if version:
            return int(version[0])
    else:
        r = re.findall(r'.+product\x00Maya (\d+).+', line, re.I)
        if r:
            return int(r[0])
        r = re.findall(r'.+product\x00Maya (\d+).+', f.readline(), re.I)
        if r:
            return int(r[0])
        r = re.findall(r'.+product\x00Maya (\d+).+', f.readline(), re.I)
        if r:
            return int(r[0])
    f.close()
    return 2012


def get_maya_py(scene_name):
    maya_version = get_maya_version(scene_name)
    if os_type == 'win':
        return "C:/tools/Autodesk/Maya%s/bin/mayapy.exe" % (maya_version)
    else:
        return "/usr/autodesk/maya%s-x64/bin/mayapy" % (maya_version)


def get_current_plugins():
    f = open(r'C:\mnt\centralized_tool\currentVersion.txt', "r")
    info = [i.strip() for i in f.readlines() if i.strip()][0]
    f.close()
    return info


def get_arnold_path(scene_name):
    maya_version = get_maya_version(scene_name)
    return r"C:\tools\aas_tools\aas_tools\mtoadeploy\1.2.4.3\%s\scripts" %  maya_version


def get_arnold_shader(maya_version):
    if os_type == 'win':
        if maya_version == 2014:
            arnold_version = "1.2.4.3"
        if maya_version == 2015:
            arnold_version = '1.2.4.3'
        else:
            arnold_version = '1.2.4.3'
        return r'C:\tools\aas_tools\aas_tools\mtoadeploy\%s\%s\shaders' % (arnold_version, maya_version)
    else:
        # TODO: Linux maya 2015 MtoA
        return "/mnt/v/dragon/scripts/opt/mtoa_1.0.0.1/shaders"


def get_arnold_default_shader(maya_version):
    if os_type == 'win':
        if maya_version == 2011:
            arnold_version = 0.18
        elif maya_version == 2014:
            arnold_version = "1.2.4.3"
        elif maya_version == 2015:
            arnold_version = '1.2.4.3'
        else:
            arnold_version = 0.23
        return r'C:\tools\aas_tools\aas_tools\mtoadeploy\%s\%s\shaders' % (arnold_version, maya_version)
    else:
        return None


def get_arnold_kick(maya_version):
    if os_type == "win":
        if maya_version == 2011:
            arnold_version = 0.18
        elif maya_version == 2014:
            arnold_version = "1.2.4.3"
        elif maya_version == 2015:
            arnold_version = '1.2.4.3'
        else:
            arnold_version = 0.23
        return r"C:\tools\aas_tools\aas_tools\mtoadeploy\%s\%s\bin\kick.exe" % (arnold_version, maya_version)
    else:
        # TODO: Linux maya 2015 MtoA
        return "/mnt/v/dragon/scripts/opt/mtoa_1.0.0.1/bin/kick"


def get_maya_batch(scene_name):
    maya_version = get_maya_version(scene_name)
    print os_type
    if os_type == 'win':
        return "C:/tools/Autodesk/Maya%s/bin/mayabatch.exe" % maya_version
    else:
        return "/usr/autodesk/maya%s-x64/bin/maya -batch" % maya_version


def get_maya_exe(scene_name):
    maya_version = get_maya_version(scene_name)
    return "C:/tools/Autodesk/Maya%s/bin/maya.exe" % maya_version


def get_mov_codes(file):
    f = open(file, "rb")
    head = f.read(1000)
    f.close()
    r = re.findall(
        r"stsd.+?[\x00\x01].{1}([a-zA-Z]+)\x00.+\x01([a-zA-Z]+)\x00.+\x01[\n\r]([\w ]+)\x00", head)
    if r:
        return r[0]


def copy(src, dst):
    if os.path.exists(src):
        if os.path.isfile(src):
            if os.path.splitext(dst)[1]:
                if not os.path.isdir(os.path.dirname(dst)):
                    os.makedirs(os.path.dirname(dst))
                shutil.copy2(src, dst)


def clear_folder(path):
    try:
        if os.path.isdir(path):
            files = [os.path.join(path, i) for i in os.listdir(path)]
            for file in files:
                if os.path.isdir(file):
                    clear_folder(file)
                    try:
                        os.rmdir(file)
                    except:
                        pass
                else:
                    try:
                        os.remove(file)
                    except:
                        pass
    except:
        pass


def gran_screen(*args):
    from PIL import ImageGrab
    im = ImageGrab.grab(*args)
    out = cStringIO.StringIO()
    im.save(out, "PNG")
    out.seek(0)
    result = out.read()
    out.close()
    return result


def get_mov_info(mov):
    import subprocess
    mediainfoExe = os.path.join(os.path.dirname(
        __file__), 'software', "MediaInfo.exe")
    if os.path.exists(mediainfoExe):
        p = subprocess.Popen("\"%s\" %s" % (mediainfoExe, mov),
                             shell=1, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             )
        # sometimes, a mov has multi tracks. such like video track and sound track.
        # And sound track's duration maybe different than video's.
        # we must ignore the sound info.
        result = p.communicate()[0]
        result = result.replace("\r\n", "//")

        if "Audio" in result:
            result = re.findall('(.+)Audio.+', result, re.I)[0]

        info = dict([[j.strip() for j in i.split(" : ")]
                    for i in result.split("//") if ":" in i])
        print info
        info["Width"] = "".join(re.findall(r'(\d+)', info["Width"]))
        info["Height"] = "".join(re.findall(r'(\d+)', info["Height"]))
        info["Frame rate"] = re.findall(r'(\d+\.\d+).+', info["Frame rate"])[0]
        second = re.findall(r'(\d+)s', info["Duration"])[0] if \
            re.findall(r'(\d+)s', info["Duration"]) \
            else 0
        microSecond = re.findall(r'(\d+)ms', info["Duration"])[0] if \
            re.findall(r'(\d+)ms', info["Duration"]) \
            else 0

        info["Duration"] = "%.3f" % (int(second)+int(microSecond)/1000.000)
        info["frames"] = int(round(float(info[
                             "Duration"])*float(info["Frame rate"])))
        info["aspect"] = "%s*%s" % (info["Width"], info["Height"])
        return info


def get_image_info(image):
    import subprocess
    djvExe = os.path.join(os.path.dirname(__file__), 'software', "djv", "bin", "djv_info.exe")
    result = {}
    if os.path.exists(djvExe):
        p = subprocess.Popen("\"%s\" %s -v" % (djvExe, image),
                             shell=1, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             )
        info = dict([[j.strip() for j in i.split("=")]
                    for i in p.communicate()[0].split("\n")
                    if "=" in i])
        info["aspect"] = "%s*%s" % (info["Width"], info["Height"])
        return info


def is_tx_bad(txFile):
    # imageio need import specifily, because qube is 32bit and can't load
    # imageio.
    try:
        image = imageio.read(txFile)
        data = image.read_data()
        image.close()
        return 0
    except:
        import sys
        print sys.exc_info()
        return 1


if __name__ == "__main__":
    pass
