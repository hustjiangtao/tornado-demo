-- Create a new table named post

-- drop table if exists post;
create table if not exists post (
id INTEGER primary key AUTOINCREMENT ,
title varchar(100) not null ,
author varchar(50) not null ,
tag varchar(32) ,
intro varchar(300) ,
content text ,
format varchar(10) ,
source varchar(10) ,
source_id varchar(64) ,
original_url varchar(128) ,
original_url timestamp default (datetime('now', 'localtime')) ) ;