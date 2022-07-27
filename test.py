import argparse
import json
import logging
import datetime

from simple_tg_notifier import SimpleTgNotifier
from email_notifier import EmailNotifier


FORMAT = '%(asctime)s %(levelname)s:%(name)s:%(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

def parse_argument():
    parser = argparse.ArgumentParser(description='Shopee daily checkin bot.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_argument()

    tg_bot = SimpleTgNotifier('credential/telegram.json')
    tg_bot.send_message('Hello 嗨, 現在時間  %s' % datetime.datetime.now())

    mail_notifier = EmailNotifier('credential/email.json')
    mail_notifier.send_message('Hello 嗨, 現在時間 %s' % datetime.datetime.now(), receiver='yspan2k@gmail.com')
