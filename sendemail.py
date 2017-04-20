# -*- coding:utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sendEmail():
	# 输入Email地址和口令:
	from_addr = 'xn4923@163.com'
	password = 'fha49888'
	# 输入收件人地址:
	to_addr = '327678269@qq.com'
	# 输入SMTP服务器地址:
	smtp_server = 'smtp.163.com'

	msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
	msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
	msg['To'] = _format_addr('BCT <%s>' % to_addr)
	msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()
	
sendEmail();