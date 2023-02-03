CREATE DATABASE IF NOT EXISTS `test1`;
use test1;
create table `user` (`id` int auto_increment not null primary key, `username` varchar(255) not null, `pwd_sha256` char(64) not null, `groupname` varchar(255) not null, `role` varchar(255) not null);
create table `groups` (`id` int auto_increment not null primary key,`groupname` varchar(255) not null);
create table `domains` (`id` int auto_increment not null primary key,`domain` varchar(255) not null);
create table `root` (`id` int auto_increment not null primary key, `domain` varchar(255) not null, `record_detail` varchar(255) not null, `record_type` int not null,`groupname` varchar(255) not null,`user` varchar(255));
insert into `user` (`username`, `pwd_sha256`,`groupname`,`role`) values ('admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918','root','admin');