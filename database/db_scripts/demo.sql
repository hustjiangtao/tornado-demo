-- Create a new table named xxx

-- drop table if exists demo;
create table if not exists demo (
id INTEGER primary key AUTOINCREMENT ,
name varchar(50) not null unique ,
create_time timestamp default (datetime('now', 'localtime')) ) ;