# The MySQL Audit archive 
## MySQL Audit once it is enabled and data is logged.  It can be read using "audit_log_read" function.
## - the "audit_log_read" function has a buffer "audit_log_read_buffer_size" which determine how much data it can be read in a single call.  The default size is 32k.
## - This python program is to retrieve ALL the audit log with setting of audit_log_read_buffer_size=4194304.
##   Each time the "audit_log_read" function is called, the JSON record is parsed and the records are created to the audit_archive.audit_data table.
##   The audit_log_read function has argument to determine the start point to read.   The function call is invoked with the last timestamp record info until there is no more data to read.
##
## Reference : https://dev.mysql.com/blog-archive/mysql-audit-data-consolidation-made-simple/

1. Firstly to create the DB and Table
2. Change the auditarchive.py with default variables to connect to DB (ip, port, user, password)
3. The python program can be executed using mysqlsh
   . mysqlsh --py < auditarchive.py 


Note :
The archive process creates records and it may trigger AUDIT records.  Eventually, the program may run indefinitely.
So, the archive process should be executed with a user having a filter rule to 'no-log'

There are 2 python program.  
- auditarchive3.py : It reads the audit records and insert the data to audit_data 
- auditarchive_rename.py : Each time it starts, it renames the audit_data to audit_data_<timestamp> if the audit_data is not an empty table.   New reocrds are written to audit_data table.




   
