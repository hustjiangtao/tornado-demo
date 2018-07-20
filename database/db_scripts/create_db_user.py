# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Create table user"""


from database.models.base_model import Session


def main():
    """run to exec"""
    create_sql = """
    -- drop table if exists user;
    create table if not exists user (
    id INTEGER primary key AUTOINCREMENT ,
    name varchar(50) not null unique ,
    email varchar(50) not null unique ,
    mobile varchar(20) ,
    password char(64) ,
    salt char(10) ,
    create_time timestamp default (datetime('now', 'localtime')) ) ;
    """

    session = Session()

    result = session.execute(create_sql)
    print(result)
    if result:
        print('create table user success.')
    else:
        print('create table user failed.')


if __name__ == "__main__":
    main()
