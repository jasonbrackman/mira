# -*- coding: utf-8 -*-
import getpass
import sys
from miraLibs.dbLibs import db_api


def get_department_of_user(user_name=None):
    if not user_name:
        user_name = getpass.getuser()
    db = db_api.DbApi().db_obj
    department = db.get_user_department(user_name)
    return department


if __name__ == "__main__":
    print get_department_of_user("heshuai")

