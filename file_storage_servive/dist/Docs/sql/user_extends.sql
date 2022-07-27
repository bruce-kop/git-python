create table if not exists `user_extends`(
`id` VARCHAR(128) not null,
`user_id` VARCHAR(128) not null,
`is_online` INT not null default 0,
`field` VARCHAR(128) not null,
`value` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;