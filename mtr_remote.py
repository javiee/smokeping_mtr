#!/usr/bin/env python
"""
The script is developed to work with smokeping. It accepts 5 arguments name-of-alert, target, loss-pattern, rtt-pattern, hostname
http://oss.oetiker.ch/smokeping/doc/smokeping_config.en.html
To test the scripts ./mrt_remote.py alert [target ip] loss-pattern rtt-pattern hostname
Scripts assumes that ssh connections are passwordless using key authentication
"""
import argparse 
import subprocess
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVERS = ['server1', 'server2', 'server3']
EMAIL_TO = 'to@mail.com'
EMAIL_FROM = 'your@mail.com'
mail = MIMEMultipart('alternative')
#logging config
logger = logging.getLogger('smokeping MTR')
logger.setLevel(logging.DEBUG)
smoke_log = logging.FileHandler('/var/log/smokeping.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
logger.addHandler(smoke_log)
smoke_log.setFormatter(formatter)

class Main (object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='Stores arguments into the variables')
        parser.add_argument('alert', action="store")
        parser.add_argument('target', action="store")
        parser.add_argument('loss', action="store")
        parser.add_argument('rtt', action="store")
        parser.add_argument('hostname', action="store")
        args = parser.parse_args()
	logger.debug('ALERT has been triggered, alert:%s, target:%s, loss:%s,rtt:%s, hostname %s'%(args.alert, args.target, args.loss, args.rtt, args.hostname))
        self.mtr_remote(args)

    def mtr_remote(self, args):
        body = []
        for host in SERVERS:
            body.append ('MTR run from %s \n\n'% host)
            command = "/usr/bin/ssh -o 'UserKnownHostsFile ~/.ssh/KnownHosts' -i /etc/smokeping/.ssh/id_rsa mtr@%s /usr/bin/mtr --report --report-cycles 5 %s"%(host, args.target)
	    try:
            p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
	    except:
            logger.debug('MTR from %s has failed'%host)
            pass 
            logger.debug('MTR from %s successful'%host)
        body.append(p.communicate()[0])
	    body.append('\n')
        #concatenated elements of the list in a string
        message = ''.join(body)
        #Send the results through mail
        self.send_mail(args.hostname, args.target, message)
            
    def send_mail(self, host, target, body):
        mail['Subject']= "Subject: smokeping detected loss to %s - %s"%(target, host)
        mail['from'] = EMAIL_FROM
        mail['to'] = EMAIL_TO
        text = body
        part = MIMEText(text, 'plain')
        mail.attach(part)
        #send the mail
        s = smtplib.SMTP('localhost')
        try:
            s.sendmail(EMAIL_FROM, EMAIL_TO, mail.as_string())
            logger.debug('MAIL succesfully sent to %s'%EMAIL_TO)
            s.quit()
        except:
            logger.debug('MAIL has failed, please check mail.log')
            pass 
if __name__== "__main__":
    main = Main()

