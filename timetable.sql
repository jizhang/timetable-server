create table event (
  id int not null primary key auto_increment
  ,title varchar(2000) not null
  ,category_id int not null
  ,`start` datetime not null
  ,`end` datetime not null
  ,created datetime not null
  ,updated timestamp not null default current_timestamp on update current_timestamp
  ,index idx_start (`start`)
);

create table note (
  id int not null primary key auto_increment
  ,content text not null
  ,created datetime not null
);
