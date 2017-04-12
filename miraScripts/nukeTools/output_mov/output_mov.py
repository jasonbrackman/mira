#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """
import os
import sys
import re


def get_input():
    args = nuke.rawArgs
    if len(args) < 5:
        sys.exit(1)
    else:
        folder = args[3]
        fps = args[4]
        return folder, fps


def get_frames(folder):
    all_frames = os.listdir(folder)
    if 'Thumb.db' in all_frames:
        all_frames.remove('Thumb.db')
    all_frames = [frame for frame in all_frames
                  if os.path.isfile(os.path.join(folder, frame))]
    return all_frames


def get_frame_range(folder):
    all_frames = get_frames(folder)
    if all_frames:
        pattern_frame = r'.*\.(\d{4})\.(exr|png|jpg|jpeg|tga|tif|EXR|PNG|TGA|JPG|JPEG|TIF)'
        frame_numbers = [int(re.match(pattern_frame, frame).group(1))
                         for frame in all_frames
                         if re.match(pattern_frame, frame)]
        start_frame, end_frame = [min(frame_numbers), max(frame_numbers)]
        if len(frame_numbers) == end_frame - start_frame + 1:
            return start_frame, end_frame
        else:
            return None
            # cmd = "@echo msgbox \"%s frame lost\" >msg.vbs" % folder
            # os.system(cmd)
            # cmd = "@msg.vbs"
            # os.system(cmd)
            # cmd = "del msg.vbs"
            # os.system(cmd)


def get_frame_profile(folder):
    all_frames = get_frames(folder)
    if all_frames:
        replaced_frame = re.sub(r'\.\d{4}', '.%04d', all_frames[0])
        return os.path.join(folder, replaced_frame)


def get_output_dir(folder):
    mov_dir = os.path.join(os.path.dirname(folder), 'mov')
    if not os.path.isdir(mov_dir):
        os.makedirs(mov_dir)
    mov_name = os.path.join(mov_dir, '%s.mov' % os.path.basename(folder))
    mov_name = mov_name.replace('\\', '/')
    return mov_name


def create_read_node(folder, start_frame, end_frame):
    read_file_name = get_frame_profile(folder)
    read_file_name = read_file_name.replace('\\', '/')
    read_node = nuke.nodes.Read(file=read_file_name)
    read_node['first'].setValue(start_frame)
    read_node['last'].setValue(end_frame)
    read_node['origfirst'].setValue(start_frame)
    read_node['origlast'].setValue(end_frame)
    return read_node


def create_write_node(folder):
    file_name = get_output_dir(folder)
    write_node = nuke.nodes.Write(file=file_name)
    write_node['channels'].setValue('rgb')
    write_node['file_type'].setValue('mov')
    write_node['colorspace'].setValue(2)
    try:
        write_node['meta_codec'].setValue(21)
    except:
        write_node['codec'].setValue(13)
    write_node['meta_encoder'].setValue(0)
    write_node['mov64_fps'].setValue(25)
    return write_node


def set_fps(fps_value):
    nuke.root()['fps'].setValue(fps_value)


def main():
    import nuke
    folder, fps_value = get_input()
    folder = folder.replace('\\', '/')
    # create read node
    if get_frame_range(folder):
        start_frame, end_frame = get_frame_range(folder)
        # set_fps
        set_fps(int(fps_value))
        # create read node
        read_node = create_read_node(folder, start_frame, end_frame)
        # create write node
        write_node = create_write_node(folder)
        write_node.setInput(0, read_node)
        # execute
        nuke.execute(write_node, start_frame, end_frame, continueOnError=True)
        nuke.scriptClose()


if __name__ == '__main__':
    main()
