drop table `grouprole`;
create table if not exists `grouprole`(
`id` integer not null auto_increment,
`role_name` VARCHAR(128) not null,
`note` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;