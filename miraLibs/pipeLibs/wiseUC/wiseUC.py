#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'

import sendMail








def send_person_msg(sendname, receive, title, content, url,logger=None):
    my_mail = sendMail.SendMail()
    my_mail.send_message(sendname, receive, title, content, url,logger)


#This function is invalid
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'Z:\mira\miraLibs\site-packages\py27')
# import urllib
import json
import logging
# from SOAPpy import WSDL
from SOAPpy import SOAPProxy

host = 'http://192.168.0.200'
port = 14132
keycode = 'gzRN53VWRF9BYUXo'
password = '666666'
encode ='utf-8'
# if sys.executable.endswith('maya.exe'):
#     encode = 'gb2312'


def get_id(user_name):
    pid = -1
    server = SOAPProxy(host + ':' + str(port) + '/Interface/www/soap/stdserver.php?wsdl')
    response = server.getjid(user_name.decode(encoding=encode), password, keycode)
    # print response.msg
    if response.flag:
        pid = json.loads(response.msg)['PID']
    print pid
    return pid


def exist_account(user_name, kind):

    server = SOAPProxy(host + ':' + str(port) + '/Interface/www/soap/stdserver.php?wsdl')

    response = server.chkisset(keycode, user_name.decode(encoding=encode), kind, 2)
    print response.msg
    return response.flag



# This function is invalid

def send_person_msg(sendname, receive, title, content, url,logger=None):
    if not logger:
        logger = logging.getLogger()

    # data = {
    #     "sendname": '赵鹏',
    #     "receive": '何帅',
    #     "title": '测试发送',
    #     "content": 'happy',
    #     "url": wiseuc_url,
    #     "style": 1,
    #     "keycode": 'key'
    # }

    # postdata = urllib.urlencode(data)
    # print postdata
    #
    # # req = urllib2.Request(rtx_url, postdata)
    # # print req
    # # response = urllib2.urlopen(req)
    # #
    # # print response
    # #
    # # doc = urllib.urlopen(rtx_url).read()
    # # print doc
    # #
    # # post_data = {}
    # # post_data['status'] = 1
    # # post_data['info'] = "success"
    # #
    # # json_doc = json.loads(urllib.urlopen(rtx_url).read())
    #
    # dd = json.dumps(data)
    # print data
    # print dd

    # server = WSDL.Proxy(wiseuc_url)
    # print server
    # print server.methods['sendmsg'].inparams[0].name
    # print server.methods['sendmsg'].inparams[0].type
    # print server.show_methods()

    msg = None

    if get_id(sendname) == -1:
        logger.info('sendname invalid')
        print 'sendname invalid'
    if get_id(receive) == -1:
        logger.info('rec name invalid')
        print 'rec name invalid'

    if get_id(sendname) != -1 and get_id(receive) != -1:

        if not not len(title):
            server = SOAPProxy(host+':'+str(port)+'/Interface/www/soap/stdserver.php?wsdl')

            response = server.sendmsg(sendname.decode(encoding=encode),
                                      receive.decode(encoding=encode),
                                      title.decode(encoding=encode),
                                      content.decode(encoding=encode),
                                      url.decode(encoding=encode),
                                      1,
                                      keycode.decode(encoding=encode))
            msg = response.msg
            logger.info('wiseUC success')
            print 'wiseUC success'
    else:
        logger.info('wiseUC failed')
        print 'wiseUC failed'
    logger.info(msg)
    return msg


# def send_group_msg(sendname, receive, title, content, url):
#
#     # data = {
#     #     "sendname": '赵鹏',
#     #     "receive": '何帅',
#     #     "title": '测试发送',
#     #     "content": 'happy',
#     #     "url": wiseuc_url,
#     #     "style": 1,
#     #     "keycode": 'key'
#     # }
#
#     # postdata = urllib.urlencode(data)
#     # print postdata
#     #
#     # # req = urllib2.Request(rtx_url, postdata)
#     # # print req
#     # # response = urllib2.urlopen(req)
#     # #
#     # # print response
#     # #
#     # # doc = urllib.urlopen(rtx_url).read()
#     # # print doc
#     # #
#     # # post_data = {}
#     # # post_data['status'] = 1
#     # # post_data['info'] = "success"
#     # #
#     # # json_doc = json.loads(urllib.urlopen(rtx_url).read())
#     #
#     # dd = json.dumps(data)
#     # print data
#     # print dd
#
#     # server = WSDL.Proxy(wiseuc_url)
#     # print server
#     # print server.methods['sendmsg'].inparams[0].name
#     # print server.methods['sendmsg'].inparams[0].type
#     # print server.show_methods()
#
#     msg = None
#
#     if exist_account(sendname, 3) and exist_account(receive, 3):
#
#         if not not len(title):
#             server = SOAPProxy(host+':'+str(port)+'/Interface/www/soap/stdserver.php?wsdl')
#
#             response = server.sendmsg(sendname.decode(encoding=encode),
#                                       receive.decode(encoding=encode),
#                                       title.decode(encoding=encode),
#                                       content.decode(encoding=encode),
#                                       url.decode(encoding=encode),
#                                       0,
#                                       keycode.decode(encoding=encode))
#             msg = response.msg
#             print response.msg
#     return msg


def send_persons_msg(sendname, receives, title, content, url):

    # data = {
    #     "sendname": sendname,
    #     "receive": receives[1],
    #     "title": title,
    #     "content": content,
    #     "url": url,
    #     "style": 1,
    #     "keycode": keycode
    # }
    #
    # #
    # # postdata = urllib.urlencode(data)
    # # print postdata
    # #
    # # # req = urllib2.Request(rtx_url, postdata)
    # # # print req
    # # # response = urllib2.urlopen(req)
    # # #
    # # # print response
    # # #
    # # # doc = urllib.urlopen(rtx_url).read()
    # # # print doc
    # # #
    # # # post_data = {}
    # # # post_data['status'] = 1
    # # # post_data['info'] = "success"
    # # #
    # # # json_doc = json.loads(urllib.urlopen(rtx_url).read())
    # #
    #
    # dd = json.dumps(data)
    # print data
    # print dd

    # server = WSDL.Proxy(wiseuc_url)
    # print server
    # print server.methods['sendmsg'].inparams[0].name
    # print server.methods['sendmsg'].inparams[0].type
    # print server.show_methods()

    # if exist_account(sendname, 3) and exist_account(receive, 3):
    #
    #     if not not len(title):

    server = SOAPProxy(host+':'+str(port)+'/Interface/www/soap/stdserver.php?wsdl')
    info = []

    if get_id(sendname) != -1:

        for receive in receives:
            if get_id(receive) == -1:
                continue
            else:
                per_info = '{\'sendname\':'\
                     + sendname.decode(encoding=encode)\
                     + ',\'receive\':'\
                     + receive.decode(encoding=encode)\
                     + ',\'title\':'\
                     + title.decode(encoding=encode)\
                     + ',\'content\':'\
                     + content.decode(encoding=encode)\
                     + ',\'url\':'\
                     + url.decode(encoding=encode)\
                     + ',\'style\':'\
                     + str(1)\
                     + ',\'keycode\':\''\
                     + keycode.decode(encoding=encode)\
                     + '\'}'
                info.append(per_info)
    response = server.sendmsgs(json.dumps(info).decode(encoding=encode))
    print response


def main(*args):
    sender = args[1]
    acceptor = args[2]
    title = args[3]
    content = args[4]
    link = args[5]
    send_person_msg(sender, acceptor, title, content, link)
'''
if __name__ == "__main__":
    # main(sys.argv)
    send_person_msg(u'admin',u'xiedonghang', u'测试标题', u'发送给小吉的测试内容', u'','')
    # send_persons_msg('何帅', ['何帅', '赵鹏', '单位'], '测试标题', '发送给happy的测试内容', '')
    # send_group_msg('何帅', '匠人坊/TD', '测试标题', '群发送给happy的测试内容', '')