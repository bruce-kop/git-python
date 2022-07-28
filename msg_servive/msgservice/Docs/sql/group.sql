create table if not exists `group`(
`id` VARCHAR(128) not null,
`name` VARCHAR(128) not null,
`QR_code` VARCHAR(1024),
`notice` VARCHAR(1024),
`note` VARCHAR(512),
PRIMARY KEY (`id`)
)default charset=utf8mb4;