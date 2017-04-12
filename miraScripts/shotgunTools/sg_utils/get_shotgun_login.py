#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_libs_get_shotgun_login
# description : ''
# author      : Aaron Hui
# date        : 2015/12/16
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import getpass
import sys
# Third-party modules
sys.path.insert(0, r'Z:/Resource/Support/aas_repos/aas_libs/site-packages')
from suds.client import Client
# Studio modules

# Local modules


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_libs_get_shotgun_login_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def get_shotgun_login():
    user_name = getpass.getuser()
    url = "http://shareservice.ants.com/EmployeeWS.asmx?wsdl" #接口的URL
    client = Client(url)
    request = client.factory.create('GetShotgunLogin')
    request.dominAccount = user_name
    return client.service.GetShotgunLogin(request)


if __name__ == "__main__":
    print get_shotgun_login()
