drop table `user`;
create table if not exists `user`(
`id` VARCHAR(128) not null,
`name` VARCHAR(128) not null unique,
`avatar` VARCHAR(512),
`phone` VARCHAR(32) unique,
`pwd` VARCHAR(512),
`created_at` timestamp,
`updated_at` timestamp,
PRIMARY KEY (`id`)
)default charset=utf8mb4;