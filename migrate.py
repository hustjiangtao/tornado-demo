# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""db migrate execute by google fire
based alembic
alembic revision -m "<version>"
alembic upgrade <version>
alembic upgrade head
alembic downgrade <version>
alembic downgrade head
see more: alembic --hep
"""


import os
import fire


class Migrate:

    """db migrate"""

    def __execute(self, cmd):
        """execute cmd
        :param cmd: cmd to exec
        """
        os.system(f"""pipenv run {cmd}""")

    def commit(self, msg):
        """generate version
        :param msg: str, msg to commit
        """
        # print(f'alembic revision --autogenerate -m "{msg}"')
        self.__execute(f'alembic revision --autogenerate -m "{msg}"')
        # self.__execute(f'alembic current')

    def upgrade(self, version):
        """upgrade to version
        :param version: version to upgrade
        """
        self.__execute(f'alembic upgrade {version}')

    def downgrade(self, version):
        """downgrade to version
        :param version: version to downgrade
        """
        self.__execute(f'alembic downgrade {version}')

    def upgrade_head(self):
        """upgrade to version"""
        self.__execute(f'alembic upgrade head')

    def downgrade_head(self):
        """downgrade to version"""
        self.__execute(f'alembic downgrade head')


if __name__ == '__main__':
    fire.Fire(Migrate)
