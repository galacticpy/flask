/*drop table if exists entries;*/
/*
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);*/

create table register (
  id integer primary key autoincrement,
  position text not null,
  firstname text not null,
  lastname text not null,
  emailaddr text not null,
  userid text not null,
  estid text null
);
create table codepass (
  id integer primary key autoincrement,
  username text not null,
  password blob not null,
  userid text not null
);
create table profile (
  id integer primary key autoincrement,
  company text not null,
  address text not null,
  city text not null,
  state text not null,
  zipcode blob not null,
  estid text not null,
  callinternal text null,  
  callnetwork text null,
  callbrigade text null
);
create table payroll (
  id integer primary key autoincrement,
  firstname text not null,
  lastname text not null,
  eligible text not null,
  active text not null,
  userid text null
);
create table requester (
  id integer primary key autoincrement,
  requestid text not null,
  userid text not null,
  requestsent integer not null,
  requestaccepted integer null,
  crntdate text not null,
  crnttime text not null,
  startdate text not null,
  starttime text not null,
  endtime text not null,
  requestmin integer not null,
  requestcancel text null,
  canceltime text null,
  cancelmin integer null
);
create table brigade (
  id integer primary key autoincrement,
  requestid text not null,
  brigadeid text not null,
  accepteddate text not null,
  acceptedtime text not null,
  brigadeaccepted integer null,
  brigadecancel integer null  
);