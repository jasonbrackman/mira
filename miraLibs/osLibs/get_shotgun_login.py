# -*- coding: utf-8 -*-

import getpass
from employee_web_service import employee_web_service


def get_shotgun_login():
    user_name = getpass.getuser()
    user_info = employee_web_service(user_name)
    return user_info["ShotgunLogin"]


if __name__ == "__main__":
    print get_shotgun_login()
