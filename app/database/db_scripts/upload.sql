-- Create a new table named xxx

-- drop table if exists upload;
create table if not exists upload (
id INTEGER primary key AUTOINCREMENT ,
name varchar(100) not null ,
new_name varchar(100) default null ,
size INTEGER not null ,
content_type varchar(10) not null ,
url varchar(120) not null ,
create_time timestamp default (datetime('now', 'localtime')) ) ;