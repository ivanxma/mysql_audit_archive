# The MySQL Audit archive 
## MySQL Audit once it is enabled and data is logged.  It can be read using "audit_log_read" function.
 - the "audit_log_read" function has a buffer "audit_log_read_buffer_size" which determine how much data it can be read in a single call.  The default size is 32k.
 - This python program is to retrieve ALL the audit log with setting of audit_log_read_buffer_size=4194304.
   Each time the "audit_log_read" function is called, the JSON record is parsed and the records are created to the audit_archive.audit_data table.
   The audit_log_read function has argument to determine the start point to read.   The function call is invoked with the last timestamp record info until there is no more data to read.
##

Reference : https://dev.mysql.com/blog-archive/mysql-audit-data-consolidation-made-simple/

1. Create the DB and Table [01-createTable.sh]
2. Create audit user  [02-createAuditUser.sh]
3. Setup Audit rule for log and log_nothing rules and assign to user [03-createAuditFilter.sh]
   - Assign log_nothing rule to audituser, 
   - Assign log_all to % 
## Change the auditarchive.py with default variables to connect to DB (ip, port, user, password) [auditarchive.py ]
4. The python program can be executed using mysqlsh  [04-runAuditArchive.sh]
```python
   mysqlsh --py --file auditarchive_rename.py [--host db] [--port port] [--user user] [--password password] [--rename [true|false] ]
```


Note :
a. The archive process creates records and it may trigger AUDIT records.  Eventually, the program may run indefinitely.
   So, the archive process should be executed with a user having a filter rule to 'no-log'

   The audit archive can be executed with user which it has no audit.
```sql
	SELECT audit_log_filter_set_filter('log_nothing', '{ "filter": { "log": false } }');
	SELECT audit_log_filter_set_user('audituser@%', 'log_nothing');
```

b. If there is no AUDIT record [empty table for audit_data], it retrieves from the beginning for all audit records.

c. auditarchive_rename.py : Each time it starts, it renames the audit_data to audit_data_<timestamp> if the audit_data is not an empty table.   New reocrds are written to audit_data table.  You can set --rename false so that archive continue to update the same table without rename

d. the message output : end reading -  MySQL Error (3200): Session.run_sql: audit_log_read UDF failed; Reader not initialized.
   It is normal.   Reading the audit log to end point generates the error message.




   
