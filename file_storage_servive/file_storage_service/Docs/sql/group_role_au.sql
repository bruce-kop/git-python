create table if not exists `group_role_au`(
`id` VARCHAR(128) not null,
`role_id` VARCHAR(128) not null,
`au_id` VARCHAR(128) not null,
`note` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;