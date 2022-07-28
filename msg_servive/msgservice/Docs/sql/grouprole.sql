create table if not exists `grouprole`(
`id` VARCHAR(128) not null,
`role_name` VARCHAR(128) not null,
`note` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;