# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from database.base import BaseDB


class CreateDBUser(BaseDB):
    """创建user表"""

    create_sql = """
    -- drop table if exists user;
    create table if not exists user (
    id INTEGER primary key AUTOINCREMENT ,
    name varchar(50) not null ,
    email varchar(50) not null unique ,
    mobile varchar(20) ,
    create_time timestamp default (datetime('now', 'localtime')) ) ;
    """

    def __init__(self):
        super(CreateDBUser, self).__init__()

    def run(self):
        result = self.create_db(create_sql=self.create_sql)
        print(result)
        if result:
            print('create table user success.')
        else:
            print('create table user failed.')


def main():
    create_db = CreateDBUser()
    create_db.run()


if __name__ == "__main__":
    main()
