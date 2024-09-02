


mysql -uroot -h127.0.0.1 -P3340 << EOL
	SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
	SELECT audit_log_filter_set_user('%', 'log_all');

	SELECT audit_log_filter_set_filter('log_nothing', '{ "filter": { "log": false } }');
	SELECT audit_log_filter_set_user('audituser@%', 'log_nothing');

EOL
