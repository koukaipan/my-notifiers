import json
import logging
import os
import requests

class SimpleTgNotifier():
    def __init__(self, credential_file: str, log_level=logging.INFO) -> None:
        self.init_logger(log_level)
        cred = self.get_credential(credential_file)
        self.__token__ = cred['token']
        self.__chat_id__ = cred['chat_id']
        self.base_url = 'https://api.telegram.org/bot%s/sendMessage?' % self.__token__


    def init_logger(self, log_level):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)


    def get_credential(self, credential_file: str):
        cred = {'token':'', 'chat_id':''}

        if len(credential_file) > 0:
            with open(credential_file) as f:
                __cred = json.load(f)
                cred['token'] = __cred['token']
                cred['chat_id'] = __cred['chat_id']

        if len(cred['token']) == 0 or len(cred['chat_id']) == 0:
            cred['token'] = os.getenv('token', default=None)
            cred['chat_id'] = os.getenv('chat_id', default=None)

        return cred

    def send_message(self, text: str, receiver=None):
        if receiver is None:
            receiver = self.__chat_id__
        url = self.base_url + 'chat_id=%s&text=%s' % (receiver, text)
        self.logger.debug('get url = %s' % url)
        r = requests.get(url)
        self.logger.debug('status code = %s' % r.status_code)

        return r.ok