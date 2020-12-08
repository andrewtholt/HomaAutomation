
drop table if exists house;

create table house (
    ID integer primary key,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature real
);

-- insert into ten_minutes (house_temperature) values ( 19.0 );
-- insert into ten_minutes (house_temperature) values ( 19.1 );
-- insert into ten_minutes (house_temperature) values ( 19.2 );
-- insert into ten_minutes (house_temperature) values ( 19.3 );
-- insert into ten_minutes (house_temperature) values ( 19.4 );
