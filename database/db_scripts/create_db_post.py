# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from database.base import BaseDB


class CreateDBPost(BaseDB):
    """创建post表"""

    create_sql = """
    -- drop table if exists post;
    create table if not exists post (
    id INTEGER primary key AUTOINCREMENT ,
    title varchar(100) not null ,
    content text ,
    author varchar(50) not null ,
    create_time timestamp default (datetime('now', 'localtime')) ) ;
    """

    def __init__(self):
        super(CreateDBPost, self).__init__()

    def run(self):
        result = self.create_db(create_sql=self.create_sql)
        print(result)
        if result:
            print('create table post success.')
        else:
            print('create table post failed.')


def main():
    create_db = CreateDBPost()
    create_db.run()


if __name__ == "__main__":
    main()
