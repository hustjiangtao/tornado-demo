# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""upload local md to sql"""


import os
import logging
import re

from app.database.doc import doc_db


logging.basicConfig(level=logging.INFO)


class UploadMd:

    """upload md to sql"""

    def __init__(self):
        self.base_dir = '/Users/jiangtao.work/Documents/jiangtao/github/vuepress/docs/post'

    @staticmethod
    def get_file_content(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def remove_desc(str):
        return re.sub(r'---[\s\S]*---\n\n', '', str)

    @staticmethod
    def replace_toc(str):
        return re.sub(r'\[\[toc\]\]', '[TOC]', str)

    def get_all_files(self):
        file_dirs = os.walk(self.base_dir)
        for x, y, z in file_dirs:
            # parent_dir, child_dir, file
            if os.path.isdir(x) and not y:
                category = x.split('/')[-1]
                for filename in z:
                    title = os.path.splitext(filename)[0]
                    content = self.get_file_content(os.path.join(x, filename))
                    content = self.remove_desc(content)
                    content = self.replace_toc(content)
                    item = {
                        "title": title,
                        "author": 1,
                        "category": category,
                        "content": content,
                    }
                    # # save to sql
                    # doc_db.add_doc(item)
                    logging.info('add 1.')
        return file_dirs

    def run(self):
        self.get_all_files()


def main():
    upload = UploadMd()
    upload.run()


if __name__ == '__main__':
    main()
