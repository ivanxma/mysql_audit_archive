CREATE DATABASE if not exists audit_archive;


CREATE TABLE if not exists audit_archive.audit_config (
	server_uuid varchar(45) not null primary key,
	ts timestamp  not null,
	id int not null
	);

delete from audit_archive.audit_config where server_uuid = @@server_uuid;

insert into audit_archive.audit_config 
	select @@server_uuid, m.* from  JSON_TABLE( audit_log_read_bookmark(),  '$'  COLUMNS ( ts timestamp path '$.timestamp', id int path '$.id')) m;

CREATE TABLE if not exists audit_archive.`audit_data` (
  `server_uuid` varchar(45) NOT NULL,
  `id` int NOT NULL,
  `ts` timestamp NOT NULL,
  `class` varchar(20) DEFAULT NULL,
  `event` varchar(80) DEFAULT NULL,
  `the_account` json DEFAULT NULL,
  `login_ip` varchar(200) DEFAULT NULL,
  `login_os` varchar(200) DEFAULT NULL,
  `login_user` varchar(200) DEFAULT NULL,
  `login_proxy` varchar(200) DEFAULT NULL,
  `connection_id` varchar(80) DEFAULT NULL,
  `db` varchar(40) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `connection_type` varchar(40) DEFAULT NULL,
  `connect_os` varchar(40) DEFAULT NULL,
  `pid` varchar(40) DEFAULT NULL,
  `_client_name` varchar(80) DEFAULT NULL,
  `_client_version` varchar(80) DEFAULT NULL,
  `program_name` varchar(80) DEFAULT NULL,
  `_platform` varchar(80) DEFAULT NULL,
  `command` varchar(40) DEFAULT NULL,
  `sql_command` varchar(40) DEFAULT NULL,
  `command_status` varchar(40) DEFAULT NULL,
  `query` varchar(40) DEFAULT NULL,
  `query_status` int DEFAULT NULL,
  `start_server_id` varchar(400) DEFAULT NULL,
  `server_os_version` varchar(100) DEFAULT NULL,
  `server_mysqlversion` varchar(100) DEFAULT NULL,
  `args` json DEFAULT NULL,
  `account_host` varchar(80) DEFAULT NULL,
  `mysql_version` varchar(80) DEFAULT NULL,
  `the_os` varchar(80) DEFAULT NULL,
  `the_os_ver` varchar(80) DEFAULT NULL,
  `server_id` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`server_uuid`,`id`,`ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create table if not exists audit_archive.audit_data_template like audit_archive.audit_data;


