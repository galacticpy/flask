create table edits (
  id integer primary key autoincrement,
  content text not null,
  active integer not null
);

create table posts (
  id integer primary key autoincrement,
  html text not null
);