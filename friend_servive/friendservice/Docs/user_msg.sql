
create table if not exists `user_msg`(
`id` VARCHAR(128) not null,
`user_id` VARCHAR(128) not null,
`is_send` INT  not null DEFAULT 0,
`create_at` timestamp,
PRIMARY KEY (`id`)
)default charset=utf8mb4;