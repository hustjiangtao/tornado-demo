# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Notification script for Apple Mac OS"""


class Osa:
    """osa script for Apple mac os"""
    def __init__(self):
        self.cmd = self.osa_cmd

    @staticmethod
    def osa_cmd(text):
        """Base cmd for osascript"""
        import os
        os.system(f"""osascript -e '''{text}'''""")

    def notify(self, title, content):
        """Set a notification on the right top of screen"""
        self.cmd(
            f'display notification "{content}" with title "{title}"'
        )

    def alert(self, title, content):
        """Set a alert GUI in the center of screen"""
        buttons = 'buttons {"NO", "OK"}'
        self.cmd(
            f'display alert "{title}" message "{content}" {buttons}'
        )

    def open_browser(self, url=None):
        """Activate the chrome browser and open the url if given"""
        self.cmd(f'tell application "Chrome" to activate')
        if url is not None:
            self.cmd(f'tell application "Chrome" to open location "{url}"')


def main():
    osa = Osa()
    # osa.notify('开会', '十点钟开会')
    osa.alert('Check', 'OK, you got me!')
    # osa.open_browser('https://www.baidu.com')


if __name__ == '__main__':
    main()
