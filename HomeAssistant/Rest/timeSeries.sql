
drop table if exists ten_minutes;
drop table if exists sixty_minutes;

drop trigger if exists ten_minute_rollover;

create table ten_minutes (
    ID integer primary key,
    house_temperature real,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

create trigger ten_minute_rolover
    after insert on ten_minutes
begin
--    insert into sixty_minutes (max_house_temperature,min_house_temperature,avg_house_temperature) select max(house_temperature),min(house_temperature),avg(house_temperature) from ten_minutes;
    delete from ten_minutes where rowid not in (select rowid from ten_minutes order by rowid desc limit 5);
end;

create trigger test 
    after insert on ten_minutes
when ( NEW.ID % 6 = 0)
begin
    insert into sixty_minutes (max_house_temperature,min_house_temperature,avg_house_temperature) select max(house_temperature),min(house_temperature),avg(house_temperature) from ten_minutes;
end;

create table sixty_minutes (
    ID integer primary key,
    max_house_temperature real,
    min_house_temperature real,
    avg_house_temperature real,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


insert into ten_minutes (house_temperature) values ( 19.0 );
insert into ten_minutes (house_temperature) values ( 19.1 );
insert into ten_minutes (house_temperature) values ( 19.2 );
insert into ten_minutes (house_temperature) values ( 19.3 );
insert into ten_minutes (house_temperature) values ( 19.4 );
