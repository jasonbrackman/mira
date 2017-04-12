import os
import re


def sort_key(text, length=10):
    str_num = "".join(re.findall("\d+", text))
    text = "".join(re.findall("\D", text)) + str_num.zfill(length)
    return text


def get_latest_version_dir(directory, offset=0, padding=3):
    directory = directory.replace("\\", "/")
    if not os.path.isdir(directory):
        return
    version_dirs = [i for i in os.listdir(directory)
                    if os.path.isdir(os.path.join(directory, i)) and re.match("^v\d+", i)]
    if not version_dirs:
        return
    sorted_version_dirs = sorted(version_dirs, key=lambda version: sort_key(version))
    max_version = sorted_version_dirs[-1]
    if offset == 0:
        latest_version_dir = os.path.join(directory, max_version).replace("\\", "/")
    else:
        version_num = int(max_version.split("v")[-1])
        offset_version_num = version_num + offset
        offset_version = "v"+str(offset_version_num).zfill(padding)
        latest_version_dir = os.path.join(directory, offset_version).replace("\\", "/")
    return latest_version_dir

if __name__ == "__main__":
    directory = r"W:\sct\assets\character\xiaotuotuo\shd\default\_tex"
    print get_latest_version_dir(directory, offset=1)
