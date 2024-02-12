create database if not exists ChatAPI;
CREATE USER 'chatApiAdmin'@'localhost' IDENTIFIED BY 'chatApiAsys_configdminPassword';
grant all privileges on chatapi.* to 'chatApiAdmin'@'localhost';

use chatapi;

create table if not exists users(id int auto_increment not null primary key, email varchar(50) not null,
username varchar(50) not null, isAdmin boolean not null default false,
dateCreated datetime not null default current_timestamp, lastModified datetime on update current_timestamp,
archived boolean not null default false);

create table if not exists chatapi.chats (id int auto_increment not null primary key, chatName varchar(20) default null,
dateCreated datetime not null default current_timestamp, lastModified datetime on update current_timestamp,
archived boolean default false not null);

create table if not exists chatapi.usersInChat(id int auto_increment not null primary key, UserId int not null,
chatId int not null, dateAdded datetime not null default current_timestamp,
lastModified datetime on update current_timestamp, archived boolean default false not null);

create table if not exists chatapi.messages (id int auto_increment not null primary key, ChatId int not null,
UserId int not null, messageBody text not null, datePosted datetime not null default current_timestamp,
lastModified datetime on update current_timestamp , media blob default null, mediaType varchar(20) default null,
archived boolean default false not null );

create table if not exists chatapi.reactions (id int auto_increment not null primary key, MessageId int not null,
UserId int not null, symbol varchar(5) not null, archived boolean default false not null);