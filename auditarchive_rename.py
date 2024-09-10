import sys, getopt
import datetime

def main(argv):
   global myhost
   myhost = '127.0.0.1'
   global myport 
   myport = 33400
   global myuser 
   myuser = 'audituser'
   global mypass 
   mypass = 'audituser'
   global myrename
   myrename = True
   global mynamespace
   mynamespace='none'
   global mybucket
   mybucket='none'
   global osarg
   osarg=0

   opts, args = getopt.getopt(argv,"h:P:u:p:r:b:n:",["host=","port=","user=","password=","rename=", "osbucket=", "osnamespace="])
   for opt, arg in opts:
      if opt in ("-h", "--host"):
         myhost = arg
      elif opt in ("-P", "--port"):
         myport = arg
      elif opt in ("-u", "--user"):
         myuser = arg
      elif opt in ("-p", "--password"):
         mypass = arg
      elif opt in ("-p", "--rename"):
         if arg == "false" :
            myrename = False
      elif opt in ("-n", "--osnamespace"):
         mynamespace= arg
         osarg=osarg+1
      elif opt in ("-b", "--osbucket"):
         mybucket = arg
         osarg=osarg+1


if __name__ == "__main__":
   main(sys.argv[1:])


if (osarg == 1) :
  print ("--osbucket and --osnamespace must be specified together")
  exit()  

archive_session = mysqlx.get_session( {
  'host': myhost, 'port': myport,
  'user': myuser, 'password': mypass,
  } )

read_session = mysqlx.get_session( {
  'host': myhost, 'port': myport,
  'user': myuser, 'password': mypass} )

read_session.run_sql("set audit_log_read_buffer_size=4194304")
mystart = 0
the_end = False
dumptablename = "audit_data"
audit_sql1 = ("SELECT  @@server_uuid as server_uuid, id, ts, class, event, the_account,login_ip,login_os,login_user,login_proxy,connection_id,db, "  
" status,connection_type,connect_os,pid,_client_name,_client_version, " 
" program_name,_platform,command,sql_command,command_status,query, " 
" query_status,start_server_id,server_os_version,server_mysqlversion,args, " 
" account_host,mysql_version,the_os,the_os_ver,server_id " 
"FROM " 
"JSON_TABLE " 
"( ")

audit_sqlx = "  AUDIT_LOG_READ(@nextts), " 
audit_sqly = "  AUDIT_LOG_READ(), " 

audit_sql2 = (
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

archive_session.run_sql("create table if not exists audit_archive.audit_data like audit_archive.audit_data_template")
search_args = archive_session.run_sql("select id, ts from audit_archive.audit_config where server_uuid = @@server_uuid ").fetch_one()
x = "set @nextts ='{ \"timestamp\": \"" + str(search_args[1]) + "\",\"id\":" + str(search_args[0] )+ " }'"
setnext  = read_session.run_sql(x)

while ( not the_end )  : 
  archive_empty = archive_session.run_sql("select count(*) from audit_archive.audit_data limit 1").fetch_one()
  mystart = mystart + 1

  if mystart == 1 :
    audit_sql = audit_sql1 + audit_sqlx + audit_sql2
  else :
    audit_sql = audit_sql1 + audit_sqly + audit_sql2
  

  try :
    ct1 = datetime.datetime.now();
    readaudit = read_session.run_sql(audit_sql)
    ct2 = datetime.datetime.now();
    print("Audit Row Count : " + str(archive_empty[0]), "Before :", ct1, "After :", ct2, " Duration : ", ct2 - ct1)
  except Exception as err:
    if str(err).find('MySQL Error (3200)') >= 0 :
      print("end reading - ", err)
    the_end=True
    break


  aschema=archive_session.get_schema('audit_archive')
  atable=aschema.get_table('audit_data')
  

  evt = readaudit.fetch_one_object()
  if not evt :
     break;

  # this is to skip the duplicate record from last max
  if mystart == 1 :
    evt = readaudit.fetch_one_object()
  if not evt :
     break;
         

  archive_session.start_transaction()
  while evt:
      if evt['ts'] is None :
         print("ts none")
         # the_end=True
         break
      atable.insert(evt).execute()
      evt= readaudit.fetch_one_object()
  archive_session.commit();


if mystart > 0 :
  archive_session.run_sql("replace audit_archive.audit_config select @@server_uuid, ts,id from audit_archive.audit_data order by ts desc, id desc limit 1")
  tbname ="audit_data_" +  datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  if ( myrename ) :
    dumptablename = tbname
    archive_session.run_sql("rename table audit_archive.audit_data to audit_archive." + tbname)  
  else :
    dumptablename = "audit_data"


  if osarg == 2 :
    print("dumptablename")
    shell.connect({ 'host': myhost, 'port': myport, 'user': myuser, 'password': mypass, } )
    util.dump_tables("audit_archive", [dumptablename], tbname, {"osBucketName": mybucket, "osNamespace": mynamespace,"dataOnly":"true","dialect":"csv","ocimds":"true", "triggers":"false" ,"consistent":"false"})


