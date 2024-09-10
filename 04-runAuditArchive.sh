# This is to make sure root login with audit records before doing archive
echo "*******************************"
mysqlsh --py --file auditarchive_rename.py --rename true

echo "*******************************"
mysql -t -uroot -h127.0.0.1 -P3340 << EOL
use audit_archive;
show table status;
EOL




