-- Create a new table named user

-- drop table if exists user;
create table if not exists user (
id INTEGER primary key AUTOINCREMENT ,
name varchar(50) not null unique ,
email varchar(50) not null unique ,
mobile varchar(20) ,
password char(64) not null ,
salt char(10) not null ,
create_time timestamp default (datetime('now', 'localtime')) ) ;