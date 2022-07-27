create table if not exists `group_addr_book`(
`id` VARCHAR(128) not null,
`user_id` VARCHAR(128) not null,
`group_id` VARCHAR(128) not null,
`note` VARCHAR(512),
PRIMARY KEY (`user_id`, `group_id`)
)default charset=utf8mb4;