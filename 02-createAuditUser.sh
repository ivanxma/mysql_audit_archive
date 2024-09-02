mysql -uroot -h127.0.0.1 -P3340 << EOL

drop user audituser;
create user audituser identified by 'audituser';
grant AUDIT_ADMIN on *.* to audituser;
grant all on audit_archive.* to audituser;

EOL
