# -*- coding: utf-8 -*-
import os
from OpenImageIO import OpenImageIO as oiio


def resize_image(src_image_path, dst_image_path, ratio=0.5):
    dst_image_dir = os.path.dirname(dst_image_path)
    if not os.path.isdir(dst_image_dir):
        os.makedirs(dst_image_dir)
    input_image = oiio.ImageInput.open(src_image_path)
    if not input_image:
        print 'Could not open %s "' % input_image
        print "\tError: ", oiio.geterror()
        return
    image_spec = input_image.spec()
    bit = image_spec.format
    channel_num = image_spec.nchannels
    buf_src = oiio.ImageBuf(src_image_path)
    dst = oiio.ImageBuf(oiio.ImageSpec(int(image_spec.width*ratio), int(image_spec.height*ratio), channel_num, bit))
    oiio.ImageBufAlgo.resize(dst, buf_src)
    dst.write(dst_image_path)
    dst.clear()
    buf_src.clear()
    input_image.close()


if __name__ == "__main__":
    resize_image("D:/body_dif.tif", "D:/halp.jpg")