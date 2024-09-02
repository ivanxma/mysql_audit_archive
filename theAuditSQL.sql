SELECT  @@server_uuid as server_uuid, id, ts, class, event, the_account,login_ip,login_os,login_user,login_proxy,connection_id,db,   
 status,connection_type,connect_os,pid,_client_name,_client_version, 
 program_name,_platform,command,sql_command,command_status,query, 
 query_status,start_server_id,server_os_version,server_mysqlversion,args, 
 account_host,mysql_version,the_os,the_os_ver,server_id 
FROM 
JSON_TABLE 
( 
  AUDIT_LOG_READ(@nextts), 
  '$[*]' 
  COLUMNS 
  ( 
    id INT PATH '$.id', 
    ts TIMESTAMP PATH '$.timestamp', 
    class VARCHAR(20) PATH '$.class', 
    event VARCHAR(80) PATH '$.event', 
    the_account JSON PATH '$.account', 
    login_ip VARCHAR(200) PATH '$.login.ip', 
    login_os VARCHAR(200) PATH '$.login.os', 
    login_user VARCHAR(200) PATH '$.login.user', 
    login_proxy VARCHAR(200) PATH '$.login.proxy', 
    connection_id VARCHAR(80) PATH '$.connection_id', 
    db VARCHAR(40) PATH '$.connection_data.db', 
    status INT PATH '$.connection_data.status', 
    connection_type VARCHAR(40) PATH '$.connection_data.connection_type', 
    connect_os VARCHAR(40) PATH '$.connection_data.connection_attributes._os', 
    pid VARCHAR(40) PATH '$.connection_data.connection_attributes._pid', 
    _client_name VARCHAR(80) PATH '$.connection_data.connection_attributes._client_name', 
    _client_version VARCHAR(80) PATH '$.connection_data.connection_attributes._client_version', 
    program_name VARCHAR(80) PATH '$.connection_data.connection_attributes.program_name', 
    _platform VARCHAR(80) PATH '$.connection_data.connection_attributes._platform', 
    command VARCHAR(40) PATH '$.general_data.command', 
    sql_command VARCHAR(40) PATH '$.general_data.sql_command', 
    command_status VARCHAR(40) PATH '$.general_data.status', 
    query VARCHAR(40) PATH '$.genera_data.query', 
    query_status INT PATH '$.general_data.status', 
    start_server_id VARCHAR(400) PATH  '$.startup_data.server_id', 
    server_os_version VARCHAR(100) PATH '$.startup_data.os_version', 
    server_mysqlversion VARCHAR(100) PATH '$.startup_data.mysql_version', 
    args JSON PATH '$.startup_data.args', 
    account_host VARCHAR(80) PATH '$.account.host', 
    mysql_version VARCHAR(80) PATH '$.startup_data.mysql_version', 
    the_os VARCHAR(80) PATH '$.startup_data.os', 
    the_os_ver VARCHAR(80) PATH '$.startup_data.os_version', 
   server_id VARCHAR(80) PATH '$.startup_data.server_id' 
   ) 
) AS auditdata;     
