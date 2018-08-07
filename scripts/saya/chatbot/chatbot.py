# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Chatbot services base on chatterbot
> pip install chatterbot
"""


from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class Bot:
    """Bot base on chatterbot"""

    def __init__(self, name="saya"):
        """Init a bot and train it with chinese cropus"""
        self.bot = ChatBot(name)
        self.bot.set_trainer(ChatterBotCorpusTrainer)

        # self.bot.train("chatterbot.corpus.english")
        self.bot.train("chatterbot.corpus.chinese")

    def manual_train(self):
        """Train the bot manually"""
        pass

    def get_result(self, text):
        """Get result from chatterbot response"""
        result = self.bot.get_response(text)
        return result


def main():
    bot = Bot()
    while 1:
        text = input("> ")
        if 'bye' in text.lower():
            print("bye bye...")
            break
        print(bot.get_result(text))


bot = Bot()
__all__ = (
    "bot",
)


if __name__ == '__main__':
    main()
