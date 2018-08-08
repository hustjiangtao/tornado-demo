# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Backup chrome bookmarks and get simple statistical count"""


class CBB:
    """Backup for chrome bookmarks"""

    def __init__(self):
        self.bookmarks = "~/Library/Application\ Support/Google/Chrome/Default/Bookmarks"
        self.temp = './Bookmarks'
        self.data = []

    def copy_to_temp(self):
        """Copy bookmarks to local as temp"""
        import os
        if not os.path.exists(self.temp):
            os.system(f'cp {self.bookmarks} {self.temp}')
            print("temp bookmarks not exists, copied from chrome completed.")

    def read_bookmarks(self):
        """Read the bookmarks data"""
        with open(self.temp, 'rb') as f:
            bs = f.read()
        result = self.parse_bookmarks(bs)
        print(f"Total bookmarks: {len(result)}\n")
        return result

    def parse_bookmarks(self, data):
        """Parse bookmarks from file"""
        import json
        bookmarks = json.loads(data).get('roots').get('bookmark_bar')
        children = bookmarks.get('children')
        self.deep_search(children)
        return self.data

    def deep_search(self, data):
        """Search from dict"""
        for x in data:
            if "url" in x.keys():
                result = (x.get('name'), x.get('url'))
                self.data.append(result)
            if x.get('children'):
                self.deep_search(x.get('children'))

    def get_url_count(self):
        """Bookmarks statistical count"""
        result = self.data
        if not result:
            print("No result found.")
            return None
        from collections import defaultdict
        from urllib.parse import urlsplit
        count_dict = defaultdict(int)
        for name, url in result:
            host = urlsplit(url).netloc
            # count_dict[(name, host)] += 1
            count_dict[host] += 1
        for x, c in sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
            if c > 1:
                print(x, ':', c)

    def run(self):
        """Run server"""
        self.copy_to_temp()
        self.read_bookmarks()
        self.get_url_count()


def main():
    cbb = CBB()
    cbb.run()


if __name__ == '__main__':
    main()
