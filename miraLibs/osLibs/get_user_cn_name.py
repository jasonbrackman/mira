# -*- coding: utf-8 -*-

import getpass
from employee_web_service import employee_web_service


def get_user_cn_name():
    user_name = getpass.getuser()
    user_info = employee_web_service(user_name)
    return user_info["CName"]

