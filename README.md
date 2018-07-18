# tornado-demo

A demo based on Python3.6 + Tornado

## Introduction

The project is build mainly using:

- Python 3.6.5
- Tornado 5.1
- SQLAlchemy 1.2.10
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
│   ├── js
│   └── upload
└── templates
    ├── demo
    ├── functools
    ├── module
    ├── post
    ├── upload
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

## handlers

## database

## static

## templates

## lib

## scripts

## crawlers

## Pipfile

## Pipfile.lock

## LICENSE
