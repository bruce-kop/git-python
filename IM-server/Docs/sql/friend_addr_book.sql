drop table `friend_addr_book`;
create table if not exists `friend_addr_book`(
`id` VARCHAR(128) not null,
`user_id` VARCHAR(128) not null,
`friend_id` VARCHAR(128) not null,
`friend_label` VARCHAR(128),
`friend_au` VARCHAR(128) not null default "1",
`note` VARCHAR(512),
PRIMARY KEY (friend_addr_book`user_id`,`friend_id` )
)default charset=utf8mb4;