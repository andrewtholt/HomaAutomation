
drop table if exists HA;

create table HA (
    entity_id varchar(32) not null unique,
    data_type varchar(32) not null,
    cmd_topic varchar(128),
    state_topic varchar(128)
);
