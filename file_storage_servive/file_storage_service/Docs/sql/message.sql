drop table`message`;
create table if not exists `message`(
`id` VARCHAR(128) not null,
`user_id` VARCHAR(128) not null,
`content` VARCHAR(1024) not null,
`from` VARCHAR(128)  not null,
`groupid` VARCHAR(512)  not null,
`is_send` INT  not null DEFAULT 0,
`create_at` timestamp,
PRIMARY KEY (`id`)
)default charset=utf8mb4;