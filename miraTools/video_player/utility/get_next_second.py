# -*- coding: utf-8 -*-


def get_next_second(now_time):
    hour, minute, sec = now_time.split(":")
    hour = int(hour)
    minute = int(minute)
    sec = int(sec)
    sec += 1
    if sec == 60:
        minute += 1
        sec = 0
    if minute == 60:
        hour += 1
        minute = 0
    next_second = "%02d:%02d:%02d" % (hour, minute, sec)
    return next_second
