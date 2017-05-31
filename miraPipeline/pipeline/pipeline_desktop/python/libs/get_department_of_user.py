# -*- coding: utf-8 -*-
import getpass


def get_department_of_user(user_name=None):
    if not user_name:
        user_name = getpass.getuser()
    return "PA"
