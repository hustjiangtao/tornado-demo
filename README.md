# tornado-demo

A demo based on Python3.6 + Tornado

## Introduction

The project is build mainly using:

- Python 3.6.5
- Tornado 6.0.2
- SQLAlchemy 1.2.15
- SQLite3
- Redis

## Tree

The Directory Structure is as bellow.

```
./
├── crawlers
├── database
│   ├── db_scripts
│   └── models
├── handlers
├── lib
├── scripts
├── static
│   ├── css
│   ├── img
│   └── js
└── templates
    ├── demo
    ├── module
    └── user

19 directories
```

## Server.py

Server.py is the main file to start the project server.
This means you can start server as easy as bellow:

```shell
$ cd tornado-demo
$ python Server.py
Tornado server start...
```

By now, you start the tornado web server.

## setting.py

This file is the settings for Tornado Application.

- `port`: set the server port, default is 9999 if not provided with command line when start the server
- `debug`: set the log debug level if it's `True`
- `autoreload`: auto start the tornado server when files has changed if it's `True`
- `static_path`: the static files path
- `template_path`: the template files path
- `cookie_secret`: set the cookie secret when using `secure_cookie`
- `xsrf_cookies`: CSRF will be protected if it's `True`
- `login_url`: the default login url when auth is failed

## urls.py

Urls.py is the routers for searching application handler,
and the regex can be used here to match handler with the url.
A handler can handle the application.

## handlers

A handler can handle a application matched the given url.

## database

SQL models and SQL operations are defined here.

## static

Static files including favicon.ico, images, css, js files and so on.

## templates

Template files.

## lib

Common functions.

## scripts

Some script files.

## crawlers

Crawler files.

## Pipfile

File about python environment.
Including pip source, python packages, packages for development and other requires.

## Pipfile.lock

Details about python packages and environment requires.

## Usage

### Alembic

Migrate databases
auto makemigrations & migrate by manage.py

- `makemigrations`: generate sql files to migrate
- `migrate`: apply to sql server

```bash
cd tornado-demo
python manage.py makemigrations "init db"
python manage.py migrate
```

### tornado server

start server by pipenv or docker-compose

- pipenv

```bash
cd tornado-demo
pipenv install [-r requirements.txt]
pipenv run python run.py [--port=80000] [--debug=True]
pipenv run python manage.py makemigrations "init db"
pipenv run python manage.py migrate
```

- docker-compose

```bash
cd tornado-demo
docker-compose build
docker-compose up -d
docker-compose run web python manage.py makemigrations "init db"
docker-compose run web python manage.py migrate
```

## LICENSE

License file. [GPL-3]
