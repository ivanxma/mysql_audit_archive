import sys, getopt
import datetime

def main(argv):
   global myhost
   myhost = '127.0.0.1'
   global myport 
   myport = 33060
   global myuser 
   myuser = 'admin'
   global mypass 
   mypass = 'admin'
   opts, args = getopt.getopt(argv,"h:P:u:p:",["host=","port=","user=","password="])
   for opt, arg in opts:
      if opt in ("-h", "--host"):
         myhost = arg
      elif opt in ("-P", "--port"):
         myport = arg
      elif opt in ("-u", "--user"):
         myuser = arg
      elif opt in ("-u", "--user"):
         myuser = arg
      elif opt in ("-p", "--password"):
         mypass = arg
   print ('host = ', myhost)
   print ('port = ', myport)
   print ('user = ', myuser)
   print ('password = ', mypass)

print (__name__)
if __name__ == "__main__":
   main(sys.argv[1:])


archive_session = mysqlx.get_session( {
  'host': myhost, 'port': myport,
  'user': myuser, 'password': mypass} )

read_session = mysqlx.get_session( {
  'host': myhost, 'port': myport,
  'user': myuser, 'password': mypass} )


read_session.run_sql("set audit_log_read_buffer_size=4194304")

while ( 1 )  : 
  archive_empty = archive_session.run_sql("select count(*) from audit_archive.audit_data limit 1").fetch_one()

  if (archive_empty[0] > 0):
     search_args = archive_session.run_sql("select id, ts from audit_archive.audit_data order by ts desc, id desc limit 1").fetch_one()
     # x = "set @nextts ='{ \"timestamp\": \"" + str(search_args[1]) + "\",\"id\":" + str(search_args[0] ) + ", \"max_array_length\": 1000 }'"
     x = "set @nextts ='{ \"timestamp\": \"" + str(search_args[1]) + "\",\"id\":" + str(search_args[0] )+ " }'"
     setnext  = read_session.run_sql(x)
     print (x)
  else:
     print("The archive is empty - get oldest audit event")
     # read_session.run_sql("set @nextts='{ \"start\": { \"timestamp\": \"2020-01-01\"}, \"max_array_length\": 1000 }'")
     read_session.run_sql("set @nextts='{ \"start\": { \"timestamp\": \"2020-01-01\"}  }'")

  
  
  audit_sql = ("SELECT  @@server_uuid as server_uuid, id, ts, class, event, the_account,login_ip,login_os,login_user,login_proxy,connection_id,db, "  
  " status,connection_type,connect_os,pid,_client_name,_client_version, " 
  " program_name,_platform,command,sql_command,command_status,query, " 
  " query_status,start_server_id,server_os_version,server_mysqlversion,args, " 
  " account_host,mysql_version,the_os,the_os_ver,server_id " 
  "FROM " 
  "JSON_TABLE " 
  "( " 
  "  AUDIT_LOG_READ(@nextts), " 
  "  '$[*]' " 
  "  COLUMNS " 
  "  ( " 
  "    id INT PATH '$.id', " 
  "    ts TIMESTAMP PATH '$.timestamp', " 
  "    class VARCHAR(20) PATH '$.class', " 
  "    event VARCHAR(80) PATH '$.event', " 
  "    the_account JSON PATH '$.account', " 
  "    login_ip VARCHAR(200) PATH '$.login.ip', " 
  "    login_os VARCHAR(200) PATH '$.login.os', " 
  "    login_user VARCHAR(200) PATH '$.login.user', " 
  "    login_proxy VARCHAR(200) PATH '$.login.proxy', " 
  "    connection_id VARCHAR(80) PATH '$.connection_id', " 
  "    db VARCHAR(40) PATH '$.connection_data.db', " 
  "    status INT PATH '$.connection_data.status', " 
  "    connection_type VARCHAR(40) PATH '$.connection_data.connection_type', " 
  "    connect_os VARCHAR(40) PATH '$.connection_data.connection_attributes._os', " 
  "    pid VARCHAR(40) PATH '$.connection_data.connection_attributes._pid', " 
  "    _client_name VARCHAR(80) PATH '$.connection_data.connection_attributes._client_name', " 
  "    _client_version VARCHAR(80) PATH '$.connection_data.connection_attributes._client_version', " 
  "    program_name VARCHAR(80) PATH '$.connection_data.connection_attributes.program_name', " 
  "    _platform VARCHAR(80) PATH '$.connection_data.connection_attributes._platform', " 
  "    command VARCHAR(40) PATH '$.general_data.command', " 
  "    sql_command VARCHAR(40) PATH '$.general_data.sql_command', " 
  "    command_status VARCHAR(40) PATH '$.general_data.status', " 
  "    query VARCHAR(40) PATH '$.genera_data.query', " 
  "    query_status INT PATH '$.general_data.status', " 
  "    start_server_id VARCHAR(400) PATH  '$.startup_data.server_id', " 
  "    server_os_version VARCHAR(100) PATH '$.startup_data.os_version', " 
  "    server_mysqlversion VARCHAR(100) PATH '$.startup_data.mysql_version', " 
  "    args JSON PATH '$.startup_data.args', " 
  "    account_host VARCHAR(80) PATH '$.account.host', " 
  "    mysql_version VARCHAR(80) PATH '$.startup_data.mysql_version', " 
  "    the_os VARCHAR(80) PATH '$.startup_data.os', " 
  "    the_os_ver VARCHAR(80) PATH '$.startup_data.os_version', " 
  "   server_id VARCHAR(80) PATH '$.startup_data.server_id' " 
  "   ) " 
  ") AS auditdata;     ")
  
  ct1 = datetime.datetime.now();
  readaudit = read_session.run_sql(audit_sql)
  ct2 = datetime.datetime.now();
  print("Audit Row Count : " + str(archive_empty[0]), "Before :", ct1, "After :", ct2, " Duration : ", ct2 - ct1)

  aschema=archive_session.get_schema('audit_archive')
  atable=aschema.get_table('audit_data')
  if (archive_empty[0] > 0 ) :
      evt = readaudit.fetch_one_object()

  evt = readaudit.fetch_one_object()


  if not evt:
     break
  while evt:
      atable.insert(evt).execute()
      evt= readaudit.fetch_one_object()
