drop table `group_role_au`;
create table if not exists `group_role_au`(
`id` integer not null auto_increment,
`role_id`integer not null,
`au_id` integer not null,
`note` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;