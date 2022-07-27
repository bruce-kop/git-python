
create table if not exists `group_user`(
`id` VARCHAR(128) not null,
`group_id` VARCHAR(128) not null,
`user_id` VARCHAR(128) not null,
`role_id` VARCHAR(128) not null,
`nickname` VARCHAR(128),
`note` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;