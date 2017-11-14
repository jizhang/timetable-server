create table note (
  id integer primary key
  ,content text
  ,created datetime
);

create table event (
  id integer primary key
  ,title text
  ,category_id int
  ,start datetime
  ,end datetime
  ,created datetime
  ,updated datetime
);
