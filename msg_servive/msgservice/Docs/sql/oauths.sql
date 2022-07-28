create table if not exists `oauths`(
`id` VARCHAR(128) not null,
`user_id` VARCHAR(128) not null,
`oauth_type` VARCHAR(128) not null,
`oauth_id` VARCHAR(128) not null,
`unionid` VARCHAR(512),
`credential` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;