# -*- coding: utf-8 -*-
from datetime import datetime


def get_week_day(day):
    week_day_dict = {
      0: u'星期一',
      1: u'星期二',
      2: u'星期三',
      3: u'星期四',
      4: u'星期五',
      5: u'星期六',
      6: u'星期天',
    }
    day = day.weekday()
    return week_day_dict[day]


def get_current_date():
    now_time = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
    week = get_week_day(datetime.now())
    current_date = "%s %s" % (now_time, week)
    current_date = current_date.encode("utf-8")
    return current_date


if __name__ == "__main__":
    print get_current_date()
