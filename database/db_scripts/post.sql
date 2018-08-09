-- Create a new table named post

-- drop table if exists post;
create table if not exists post (
id INTEGER primary key AUTOINCREMENT ,
title varchar(100) not null ,
content text ,
author varchar(50) not null ,
create_time timestamp default (datetime('now', 'localtime')) ) ;