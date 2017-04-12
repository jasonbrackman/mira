# -*- coding: utf-8 -*-
import json

from suds.client import Client


def employee_web_service(user_name):
    url = "http://shareservice.ants.com/EmployeeWS.asmx?wsdl" #接口的URL
    client = Client(url)
    request = client.factory.create('GetEmployee')
    request.dominAccount = user_name
    result_json = client.service.GetEmployee(request)
    print "json: %s" % result_json
    if not result_json:
        return
    result_dict = json.loads(result_json)[0]
    return result_dict


if __name__ == "__main__":
    pass
