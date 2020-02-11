drop table if exists location;
create table location (
  location_id int not null auto_increment primary key,
  name varchar(100) not null,
  unique (name)
) ENGINE=InnoDB;

drop table if exists attr_type;
create table attr_type (
  attr_type_id int not null auto_increment primary key,
  attr_type varchar(255) not null,
  unique (attr_type)
) ENGINE=InnoDB;

drop table if exists attr;
create table attr (
  attr_id int not null auto_increment primary key,
  attr_type_id integer not null,
  location_id integer not null,
  value varchar(255) not null,
  unique (attr_type_id, location_id, value),
  FOREIGN KEY (attr_type_id) REFERENCES attr_type (attr_type_id),
  FOREIGN KEY (location_id) REFERENCES location (location_id)
) ENGINE=InnoDB;

