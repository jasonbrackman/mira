# -*- coding: utf-8 -*-


def convert_msec(mss):
    hours = (mss % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    minutes = (mss % (1000 * 60 * 60)) / (1000 * 60)
    seconds = (mss % (1000 * 60)) / 1000
    return "%02d:%02d:%02d" % (hours, minutes, seconds)