drop table if exists location;
create table location (
  location_id integer primary key,
  name text not null,
  unique (name)
);

drop table if exists attr_type;
create table attr_type (
  attr_type_id integer primary key,
  attr_type text not null,
  unique (attr_type)
);

drop table if exists attr;
create table attr (
  attr_id integer primary key,
  attr_type_id integer not null,
  location_id integer not null,
  value text not null,
  unique (attr_type_id, location_id, value)
);
