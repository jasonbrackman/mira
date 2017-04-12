# -*- coding: utf-8 -*-
import os
import re
import sys
import shutil
from PySide import QtGui
import miraCore
from miraLibs.pyLibs import join_path


NO_USE_FILE = ["Thumbs.db"]


def get_ffmpeg_path():
    mira_bin_dir = miraCore.get_bin_dir()
    ffmpeg_dir = join_path.join_path2(mira_bin_dir, "ffmpeg/bin")
    ffmpeg_path = join_path.join_path2(ffmpeg_dir, "ffmpeg.exe")
    return ffmpeg_path


def sequence_sort_key(text, length=255):
    str_num = ''.join(re.findall(r'\d', text))
    text = ''.join(re.findall(r'\D', text)) + str_num.zfill(length)
    return text


def sort_sequence_files(files):
    files = sorted(files, key=lambda text: sequence_sort_key(text))
    return files


def get_file_list(file_dir):
    file_list = [os.path.normpath(os.path.join(file_dir, single_file))
                 for single_file in os.listdir(file_dir)
                 if single_file not in NO_USE_FILE]
    file_list = sort_sequence_files(file_list)
    return file_list


def get_format(first_frame, second_frame):
    temp_format = None
    for index, charactor in enumerate(first_frame):
        if charactor != second_frame[index]:
            prefix = first_frame[:index]
            suffix = first_frame[index+1:]
            temp_format = "%s#%s" % (prefix, suffix)
            break
    if not temp_format:
        return
    pattern = ".*[^\d](\d*)#[^\d].*"
    numbers = re.match(pattern, temp_format).group(1)
    num = len(numbers)
    path_format = re.sub(str("\d{%s}#") % num, "#"*(num+1), temp_format)
    return path_format


def get_format_by_list(file_list):
    first_frame = file_list[0]
    second_frame = file_list[1]
    return get_format(first_frame, second_frame)


def convert(ffmpeg_path, input_format, fps, output):
    cmd = "{0} -i {1} -y -c:v prores_ks -profile:v 3 -vendor ap10 -pix_fmt yuv422p10le -r {2} {3}"
    cmd = cmd.format(ffmpeg_path, input_format, fps, output)
    print cmd
    os.system(cmd)


def get_frame_numbers(file_list):
    """
    get the format of a sequence
    :param file_list: all files in a folder
    :return: eg: *******.####.exr
    """
    path_format = get_format_by_list(file_list)
    path_format = path_format.replace("\\", "/")
    num_of_special = path_format.count("#")
    pattern = re.sub("#"*num_of_special, "(\d{%s})" % num_of_special, path_format)
    frame_numbers = list()
    for frame in file_list:
        frame = frame.replace("\\", "/")
        matched = re.match(pattern, frame)
        if not matched:
            continue
        frame_number = int(matched.group(1))
        frame_numbers.append(frame_number)
    frame_numbers.sort()
    return frame_numbers


def rename_file_list(file_dir):
    dir_name, folder_name = os.path.split(file_dir)
    temp_dir = join_path.join_path2(dir_name, "_%s_temp" % folder_name)
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    shutil.copytree(file_dir, temp_dir)
    temp_file_list = get_file_list(temp_dir)
    path_format = get_format_by_list(temp_file_list)
    num_of_special = path_format.count("#")
    for index, temp_file in enumerate(temp_file_list):
        new_name = re.sub("#"*num_of_special, str(index+1).zfill(num_of_special), path_format)
        os.rename(temp_file, new_name)
    return temp_dir


def sequence_to_mov(file_dir, fps, output=None):
    # get file list
    file_list = get_file_list(file_dir)
    if len(file_list) < 2:
        print "Please select a sequence at least 2 frames"
        return
    # check lacked frame
    path_format = get_format_by_list(file_list)
    path_format = path_format.replace("\\", "/")
    num_of_special = path_format.count("#")
    frame_numbers = get_frame_numbers(file_list)
    normal_list = range(frame_numbers[0], frame_numbers[-1])
    lacked_frames = list(set(normal_list)-set(frame_numbers))
    lacked_frames = [str(lacked_frame).zfill(num_of_special) for lacked_frame in lacked_frames]
    if lacked_frames:
        message = "Lacked Frames: \n%s" % "\n".join(lacked_frames)
        app = QtGui.QApplication(sys.argv)
        QtGui.QMessageBox.critical(None, "Lack Frame error", message)
        app.exec_()
        return
    # get ffmpeg path
    ffmpeg_path = get_ffmpeg_path()
    # get output
    if not output:
        dir_name = os.path.dirname(path_format)
        folder_name = os.path.split(dir_name)[-1]
        output = join_path.join_path2(os.path.dirname(dir_name), "%s.mov" % folder_name)
    # judge first frame start form 0001
    # -if start from 0001, do convert sequence to mov
    temp_dir = None
    first_frame_number = frame_numbers[0]
    if int(first_frame_number) == 1:
        input_format = re.sub("#"*num_of_special, "%0{0}d".format(num_of_special), path_format)
    # -else copy to current folder rename it from 0001  convert it and then delete the temp
    else:
        temp_dir = rename_file_list(file_dir)
        temp_file_list = get_file_list(temp_dir)
        temp_path_format = get_format_by_list(temp_file_list)
        temp_num_of_special = temp_path_format.count("#")
        input_format = re.sub("#"*temp_num_of_special, "%0{0}d".format(temp_num_of_special), temp_path_format)
    convert(ffmpeg_path, input_format, fps, output)
    if temp_dir:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    file_dir = r"D:\test\sequence\maya"
    sequence_to_mov(file_dir, 25)
