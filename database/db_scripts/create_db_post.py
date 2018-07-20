# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Create table post"""


from database.models.base_model import Session


def main():
    """run to exec"""
    create_sql = """
    -- drop table if exists post;
    create table if not exists post (
    id INTEGER primary key AUTOINCREMENT ,
    title varchar(100) not null ,
    content text ,
    author varchar(50) not null ,
    create_time timestamp default (datetime('now', 'localtime')) ) ;
    """

    session = Session()

    result = session.execute(create_sql)
    print(result)
    if result:
        print('create table post success.')
    else:
        print('create table post failed.')


if __name__ == "__main__":
    main()
