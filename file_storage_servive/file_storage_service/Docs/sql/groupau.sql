create table if not exists `groupau`(
`id` VARCHAR(128) not null,
`au_name` VARCHAR(128) not null,
`note` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;