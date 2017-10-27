# -*- coding: utf-8 -*-
import os
import logging
import tempfile
import subprocess
import shutil
import locale
import pipeGlobal
import miraLibs.pyLibs.join_path as join_path


def get_ffmpeg_path():
    bin_dir = pipeGlobal.bin_dir
    ffmpeg_path = join_path.join_path2(bin_dir, "ffmpeg", "bin", "ffmpeg.exe")
    return ffmpeg_path


def avi_to_mov(source_path, remove_src= False, openit=False, codec="mpeg4"):
    """
    convert avi to mov with FFMPEG
    :param source_path: avi file path
    :param openit: open mov after convert
    :param codec:
    :return:
    """
    # get output name
    src_dir, ext = os.path.splitext(source_path)
    output_path = src_dir + ".mov"
    logging.info("output mov will be saved at: %s" % output_path)
    # create temp path
    temp = tempfile.TemporaryFile()
    temp.close()
    # make FFMPEG command
    FFMPEG = get_ffmpeg_path()
    command = [FFMPEG,
               "-i",
               "\"%s\"" % source_path,
               "-q:v 1", "-vcodec \"%s\"" % codec,
               "-y", "\"%s.mov\"" % temp.name]

    command = " ".join(command)
    # execute command
    p = subprocess.Popen(command.encode(locale.getpreferredencoding()),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)

    stderr, stdout = p.communicate()
    logging.info(stdout)

    if remove_src:
        # remove source file
        try:
            os.remove(source_path)
        except Exception, e:
            logging.warning("Remove output file failed: %s" % e)
    # move temp file to output path
    try:
        shutil.move("%s.mov" % temp.name, output_path)
    except Exception, e:
        logging.error(e)

    if openit:
        # open the out put file
        subprocess.Popen("explorer \"%s\"" % os.path.abspath(output_path))

if __name__ == "__main__":
    pass
