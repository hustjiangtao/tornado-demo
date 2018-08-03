# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""A self talk robot"""


import logging
# import traceback
import random
import requests

from time import time, sleep

from nltk import word_tokenize


class Talk:
    """A self talk robot"""

    def __init__(self, boss=None):
        self.boss = {
            "name": boss,
        }
        self.name = "Saya"
        self.data = {}

    @staticmethod
    def greeting():
        greetings = ['hola', 'hello', 'hi', 'Hi', 'hey!', 'hey']
        return random.choice(greetings)

    def improve_boss(self, boss_key=None, boss_info=None):
        """Get boss's personal info"""
        if all([boss_key, boss_info]):
            self.boss[boss_key] = boss_info

        name_prompt = f"{self.greeting()}, I'm {self.name}, glad to talk with you, but may I know your name?"
        print(name_prompt)
        boss_name = input("What's your name: ")
        self.boss["name"] = boss_name
        sleep(0.3)

        age_prompt = "Ok, would you mind telling me how old are you?"
        print(age_prompt)
        boss_age = input("How old are you: ")
        self.boss["age"] = boss_age
        sleep(0.3)
        print(f"Haha, {boss_name}, Nice name.")

    def get_input(self):
        """Get input result"""
        if not self.boss.get("name"):
            self.improve_boss()
        result = input(f"{self.boss['name']}: ")
        self.data[int(time())] = result
        sleep(0.3)
        result = self.get_tokenize_input(result, to_set=False)
        return result

    @staticmethod
    def get_tokenize_input(text, to_set=False):
        """Get input str tokenize"""
        result = word_tokenize(text)
        return set(result) if to_set else result

    def get_output(self, output):
        """Get output result"""
        tuling = Tuling()
        output = tuling.get_tuling_result(output)
        result = f"{self.name}: {output}"
        sleep(0.3)
        return result

    @staticmethod
    def is_bye(texts):
        """Say bye and exit"""
        bye_words = ['exit', 'bye', 'quit', 'goodbye', 'byebye']
        if set(bye_words) & {x.lower() for x in texts}:
            return True
        else:
            return False

    def talk(self):
        input_strs = self.get_input()
        if self.is_bye(input_strs):
            return 0
        output_str = self.get_output(' '.join(input_strs))
        print(output_str)
        # print(self.data)
        return 1


class Tuling:
    """Tuling bot"""

    def __init__(self):
        self.data = None
        self.url = "http://openapi.tuling123.com/openapi/api/v2"

    def get_data(self, text):
        data = {
            # "reqType":0,
            "perception": {
                "inputText": {
                    "text": text
                },
                # "inputImage": {
                #     "url": "imageUrl"
                # },
                "selfInfo": {
                    "location": {
                        "city": "上海",
                        # "province": "北京",
                        # "street": "信息路"
                    }
                }
            },
            "userInfo": {
                "apiKey": "c7b08927d1874c2c8296edc3de68e246",
                "userId": "303320"
            }
        }

        return data

    def send_post_request(self):
        """Post request"""
        res = requests.post(url=self.url, json=self.data)
        if 200 == res.status_code:
            content = res.json()
        else:
            content = None
        if content and content['intent']['code']:
            result = [x['values']['text'] for x in content['results'] if "text" == x['resultType']][0]
        else:
            result = "I can't understand..."

        return result

    def get_tuling_result(self, text):
        self.data = self.get_data(text)
        result = self.send_post_request()
        return result


def main():
    """Start entry"""
    result = 1
    talk = Talk()
    while result:
        result = talk.talk()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        logging.warning("talk start...")
        sleep(0.5)
        main()
    except KeyboardInterrupt:
        # logging.warning(traceback.format_exc())
        sleep(0.5)
        logging.warning("bye...")
    else:
        sleep(0.5)
        logging.warning("bye...")
