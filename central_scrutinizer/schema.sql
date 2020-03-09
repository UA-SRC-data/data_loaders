drop table if exists location_type;
create table location_type (
  location_type_id integer primary key,
  location_type text not null,
  unique (location_type)
);

drop table if exists location;
create table location (
  location_id integer primary key,
  location_type_id integer not null,
  location_name text not null,
  lat_lon text,
  unique (location_name),
  foreign key (location_type_id) references location_type (location_type_id)
);

drop table if exists variable;
create table variable (
  variable_id integer primary key,
  variable text not null,
  description text,
  unique (variable)
);

drop table if exists measurement;
create table measurement (
  measurement_id integer primary key,
  variable_id integer not null,
  location_id integer not null,
  value text not null,
  unique (variable_id, location_id, value),
  foreign key (variable_id) references variable (variable_id),
  foreign key (location_id) references location (location_id)
);
