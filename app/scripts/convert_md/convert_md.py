# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""convert markdown to html

Input: list, text_list
Output: list, converted_text_list
Usage:
from convert_md import ConvertMarkdown

md = ConvertMarkdown()

save html to local:
md.run() or md.run_in_pool()

get html body:
html = md.convert_md(text)
"""


import os
import logging
import markdown
import re

from multiprocessing import cpu_count
from multiprocessing import Pool  # 进程池
from multiprocessing.dummy import Pool as ThreadPool  # 线程池


logging.basicConfig(level=logging.INFO)


class ConvertMarkdown:

    """convert markdown to html"""

    def __init__(self):
        self.host = ''
        self.exts = self.__get_exts()

    @staticmethod
    def __get_exts():
        """get md extensions"""
        exts = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
        ]
        return exts

    def get_full_html(self, body):
        """get full html"""
        # static_url_prefix = 'http://demo.hujiangtao.cn/static/mdl/css/doc/'
        static_url_prefix = ''
        html = f'''
            <html lang="zh-cn">
            <head>
            <meta content="text/html; charset=utf-8" http-equiv="content-type" />
            <link href="{static_url_prefix}default.css" rel="stylesheet">
            <link href="{static_url_prefix}github.css" rel="stylesheet">
            </head>
            <body>
            {body}
            </body>
            </html>
            '''
        return html

    @staticmethod
    def remove_desc(str):
        return re.sub(r'---[\s\S]*---\n\n', '', str)

    @staticmethod
    def replace_toc(str):
        return re.sub(r'\[\[toc\]\]', '[TOC]', str)

    def convert_local_file(self, filename):
        """convert local md file to html and save"""
        with open(filename, 'r', encoding='utf-8') as f:
            input_data = f.read()

        input_data = self.remove_desc(input_data)
        input_data = self.replace_toc(input_data)

        output_data = self.convert_md(input_data)
        output_data = self.get_full_html(output_data)

        with open(f'{os.path.splitext(filename)[0]}.html', 'w') as f:
            f.write(output_data)

        return True

    def convert_md(self, text):
        """convert md text to html body with md extensions"""
        html = markdown.markdown(text, extensions=self.exts)
        # md = markdown.Markdown(extensions=self.exts)
        # html = md.convert(text)
        return html

    def convert_full_html(self, text):
        """convert md text to full html with md extensions"""
        html = markdown.markdown(text, extensions=self.exts)
        html = self.get_full_html(html)
        return html

    def run(self):
        """run in order"""
        list(map(self.convert_local_file, self.get_files()))

    def run_in_pool(self):
        """run with thread pool"""
        pool = ThreadPool(cpu_count())
        pool.map(self.convert_local_file, self.get_files())
        pool.close()
        pool.join()

    @staticmethod
    def get_files():
        """get files to handle"""
        files = [
            '2018-06-21-Tornado参考.md',
        ]
        return files


convert_md = ConvertMarkdown().convert_md
convert_full_html = ConvertMarkdown().convert_full_html

__all__ = (ConvertMarkdown, convert_md, convert_full_html)


def main():
    md = ConvertMarkdown()
    md.run()
    # md.run_in_pool()


if __name__ == '__main__':
    main()
