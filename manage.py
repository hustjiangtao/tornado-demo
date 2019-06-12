# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""db migrate execute by google fire
based alembic
alembic revision -m "<version>"
alembic upgrade <version>
alembic upgrade head
alembic downgrade <version>
alembic downgrade head
see more: alembic --help

usage:
python manage.py makemigrations ["init db"]
python manage.py migrate
"""


import os
import fire
import time

from config import SQL


class AlembicEnv:
    """make alembic ini & cleanup after alembic operations"""
    def __init__(self):
        self.filename = 'alembic.ini'
        self.old = open(self.filename, 'r').read()

    def __enter__(self):
        with open(self.filename, 'w') as f:
            f.write(self.old.format(db=SQL.get('db')))

    def __exit__(self, exception_type, exception_value, traceback):
        with open(self.filename, 'w') as f:
            f.write(self.old)


class Migrate:

    """db migrate"""

    def __execute(self, cmd):
        """execute cmd
        :param cmd: cmd to exec
        """
        # os.system(f"""docker-compose run web {cmd}""")
        os.system(f"""pipenv run {cmd}""")

    def makemigrations(self, msg=None):
        """generate version
        :param msg: str, msg to commit
        """
        # if not msg:
        #     msg = int(time.time())
        message = f'-m "{msg}"' if msg else ''
        # print(f'alembic revision --autogenerate -m "{msg}"')
        self.__execute(f'alembic revision --autogenerate {message}')
        # self.__execute(f'alembic current')

    def migrate(self):
        """upgrade to version"""
        self.__execute(f'alembic upgrade head')

    def clean(self):
        """Remove temporary files."""
        # for root, dirs, files in os.walk('.'):
        #     if '.venv' in root:
        #         continue
        #     for name in files:
        #         if name.endswith('.pyc') or name.endswith('~'):
        #             os.remove(os.path.join(root, name))
        #     for d in dirs:
        #         if os.path.join(root, d) == './__pycache__':
        #             continue
        #         if d == '__pycache__':
        #             os.rmdir(os.path.join(root, d))
        os.popen('''python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]') if '.venv' not in p]"''')
        os.popen('''python3 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__') if '.venv' not in p]"''')


if __name__ == '__main__':
    with AlembicEnv():
        fire.Fire(Migrate)
