check locks

```
SELECT * FROM sys.innodb_lock_waits;
```

check process

```
SHOW PROCESSLIST;

-- specific process
SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST WHERE ID = ?;
```

check slow_log

```
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long%';
SHOW VARIABLES LIKE 'log_output';

SELECT
start_time
, user_host
, query_time
, rows_sent
, rows_examined
, db
, CONVERT(sql_text USING utf8) AS sql_text
FROM		mysql.slow_log
ORDER BY 	query_time DESC
;
```

check table status

```
SELECT * FROM mysql.innodb_table_stats;
```
