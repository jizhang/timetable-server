create table `user` (
  id int not null primary key auto_increment
  ,username varchar(255) not null
  ,password varchar(255) not null
  ,created_at datetime not null
  ,updated_at timestamp not null default current_timestamp on update current_timestamp
  ,index idx_username (username)
);

insert into `user` values
(1, 'test', 'pbkdf2:sha256:150000$RQEmXgTI$39b2c288c2af0cc6380add124254364a910483acd0b8d1dc81260aa1649e99d5', now(), now());

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
