drop table `group`;
create table if not exists `group`(
`id` VARCHAR(128) not null,
`name` VARCHAR(128) not null,
`avatar` VARCHAR(512),
`QR_code` VARCHAR(1024),
`notice` VARCHAR(1024),
`note` VARCHAR(512),
`created_at` timestamp,
`updated_at` timestamp,
PRIMARY KEY (`id`)
)default charset=utf8mb4;