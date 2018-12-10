# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""get all emials of diyidan from exmail.qq.com"""


import logging
import requests
import traceback
import execjs


logging.basicConfig(level=logging.INFO)


class Handler(object):

    def __init__(self):
        self.cookie = self.get_cookie()

    @staticmethod
    def get_cookie():
        with open('email_cookie', 'r') as f:
            return f.read()

    @staticmethod
    def send_request(url, params=None, headers=None, is_json=True):
        try:
            response = requests.get(url=url, params=params, headers=headers, verify=False)
            if response and response.status_code == 200:
                if is_json:
                    result = response.json()
                else:
                    result = response.content
            else:
                result = None
        except Exception as e:
            result = None
            logging.warning(traceback.format_exc())

        finally:
            return result

    def save_local(self, data):
        with open('diyidan_user_email.csv', 'w') as f:
            f.writelines(data)

    def get_all_emails(self):
        url = 'https://exmail.qq.com/cgi-bin/laddr_biz?t=memtree&limit=500&partyid=8336300&action=show_party&sid=-EpPH-YItA4D20Ac,7'
        headers = {
            "Cookie": self.cookie,
        }
        result = self.send_request(url=url, headers=headers, is_json=False)
        result = execjs.eval(result.decode(encoding='GB18030'))
        user_list = result.get('data').get('oUserList')
        title_list = ['name', 'tel', 'mobile', 'slave_alias', 'pid', 'pos', 'sex', 'alias', 'birth', 'department', 'uin', '\n']
        result = [','.join(title_list)]
        for user in user_list:
            name = user.get('name')
            tel = user.get('tel')
            mobile = user.get('mobile')
            slave_alias = user.get('slave_alias')
            pid = user.get('pid')
            pos = user.get('pos')
            sex = user.get('sex')
            alias = user.get('alias')
            birth = user.get('birth')
            department = user.get('department')
            uin = user.get('uin')
            item = (name, tel, mobile, slave_alias, pid, pos, sex, alias, birth, department, uin, '\n')
            result.append(','.join(item).encode('utf-8'))
        self.save_local(result)

    def run(self):
        self.get_all_emails()


def main():
    handler = Handler()
    handler.run()


if __name__ == '__main__':
    main()
