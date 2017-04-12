# -*- coding: utf-8 -*-
import smtplib,logging
from email.mime.text import MIMEText
from email.header import Header

class SendMail:
    def __init__(self):
        self.server_ip = '192.168.0.211'
        self.domain_name = '@a.com'

    def send_message(self,sendname, receive, title, content, url,logger=None):
        if not logger:
            logger = logging.getLogger()

        sendname_domain = sendname + self.domain_name
        if isinstance(receive,list):
            receive_domain_list = [x + self.domain_name for x in receive]
        else :
            receive_domain_list = [receive + self.domain_name]

        msg = MIMEText(content,'text','utf-8')
        msg['Subject'] = title
        msg['From'] = sendname_domain
        msg['To'] = (',').join(receive_domain_list)
        s = smtplib.SMTP(self.server_ip)
        s.sendmail(sendname_domain,receive_domain_list,msg.as_string())
        s.quit()
        logger.info('send mail success!')




if __name__ == '__main__':
    test_mail = SendMail()
    test_mail.send_message(u'xiedonghang',u'heshuai',u'你大爷',u'老子这个是测试',None,None)