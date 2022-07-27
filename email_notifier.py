import json
import logging
import os
import smtplib

from email.mime.text import MIMEText

class EmailNotifier:
    def __init__(self, credential_file: str, log_level=logging.INFO) -> None:
        self.init_logger(log_level)
        email_cfg = self.get_credential(credential_file)
        if email_cfg == None:
            return

        self.sender = email_cfg['sender']
        self.__smtp_server = smtplib.SMTP(email_cfg['smtp_host'], email_cfg['port'])
        self.__smtp_server.connect(email_cfg['smtp_host'], email_cfg['port'])
        self.__smtp_server.starttls()
        login = self.__smtp_server.login(email_cfg['sender'], email_cfg['password'])
        self.logger.debug(f'SMTP login {login}')
        del email_cfg


    def __del__(self):
        if self.__smtp_server is not None:
            self.__smtp_server.quit()


    def init_logger(self, log_level):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)


    def get_credential(self, credential_file: str):
        folder_path = os.path.dirname(credential_file)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if credential_file.startswith('~'):
            credential_file = os.path.expanduser(credential_file)

        if not os.path.exists(credential_file):
            self.log.error('email config (%s) is not existed:' % credential_file)
            return None

        with open(credential_file, 'r') as f:
            self.logger.debug('Reading email config from %s' % credential_file)
            email_cfg = json.loads(f.read())
            return email_cfg
        return None

    def send_email(self, receiver: str, title: str, msg: str):
        __msg = MIMEText(msg, 'plain', 'utf-8')
        __msg['Subject'] = title
        __msg['From'] = self.sender
        __msg['To'] = receiver
        self.logger.debug('Send "%s" to %s' % (title, receiver))
        self.logger.debug('Message:\n%s' % __msg.as_string())
        self.__smtp_server.sendmail(from_addr=self.sender, to_addrs=receiver,
                                    msg=__msg.as_string())
        # msg['From'], msg['To'], msg.as_string())


    def send_message(self, msg: str, receiver=None, title=None):
        if receiver == None:
            if 'receiver' not in self.__email_cfg.keys() or self.__email_cfg['receiver'] == None or \
                len(self.__email_cfg['receiver']) == 0:
                self.logger.error('Invalid receiver address')
                return
            else:
                receiver = self.__email_cfg['receiver']

        if title == None:
            title = 'My Notification'

        self.send_email(receiver, title, msg)


    def print_email_cfg(self):
        print('smtp_host:%s, sender:%s' % (self.__email_cfg['smtp_host'], self.__email_cfg['sender']))