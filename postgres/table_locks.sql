SELECT pid, age(clock_timestamp(), query_start), usename, query, state, wait_event, wait_event_type
FROM pg_stat_activity
WHERE query != '<IDLE>' AND query NOT ILIKE '%pg_stat_activity%'
ORDER BY query_start desc

-- LOCKing processes
select pid, state, usename, query, query_start
from pg_stat_activity
where pid in (
  select pid from pg_locks l
  join pg_class t on l.relation = t.oid
  and t.relkind = 'r'
  and  t.relname like 'tablename%'
);




-- kill running query
SELECT pg_cancel_backend(procpid);

-- kill idle query
SELECT pg_terminate_backend(procpid);

-- vacuum command
VACUUM (VERBOSE, ANALYZE);

-- all database users
select * from pg_stat_activity where query not like '<%';

-- all databases and their sizes
select * from pg_user;

-- all tables and their size, with/without indexes
select datname, pg_size_pretty(pg_database_size(datname))
from pg_database
order by pg_database_size(datname) desc;

-- cache hit rates (should not be less than 0.99)
SELECT sum(heap_blks_read) as heap_read, sum(heap_blks_hit)  as heap_hit, (sum(heap_blks_hit) - sum(heap_blks_read)) / sum(heap_blks_hit) as ratio
FROM pg_statio_user_tables;

-- table index usage rates (should not be less than 0.99)
SELECT relname, 100 * idx_scan / (seq_scan + idx_scan) percent_of_times_index_used, n_live_tup rows_in_table
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- how many indexes are in cache
SELECT sum(idx_blks_read) as idx_read, sum(idx_blks_hit)  as idx_hit, (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit) as ratio
FROM pg_statio_user_indexes;

-- Dump database on remote host to file
$ pg_dump -U username -h hostname databasename > dump.sql

-- Import dump into existing database
$ psql -d newdb -f dump.sql

-- Find partition columns on all tables
select
    par.relnamespace::regnamespace::text as schema,
    par.relname as table_name,
    partnatts as num_columns,
    column_index,
    col.column_name
from
    (select
         partrelid,
         partnatts,
         case partstrat
              when 'l' then 'list'
              when 'r' then 'range' end as partition_strategy,
         unnest(partattrs) column_index
     from
         pg_partitioned_table) pt
join
    pg_class par
on
    par.oid = pt.partrelid
join
    information_schema.columns col
on
    col.table_schema = par.relnamespace::regnamespace::text
    and col.table_name = par.relname
    and ordinal_position = pt.column_index;

  /* Get all partition names for a given table */

  SELECT
    nmsp_parent.nspname AS parent_schema,
    parent.relname      AS parent,
    nmsp_child.nspname  AS child_schema,
    child.relname       AS child
FROM pg_inherits
    JOIN pg_class parent            ON pg_inherits.inhparent = parent.oid
    JOIN pg_class child             ON pg_inherits.inhrelid   = child.oid
    JOIN pg_namespace nmsp_parent   ON nmsp_parent.oid  = parent.relnamespace
    JOIN pg_namespace nmsp_child    ON nmsp_child.oid   = child.relnamespace
WHERE parent.relname='api_record_level_scored';
-----------------------------
AUTO VACCUM and AUTO ANALYZE
-----------------------------

-- Is AutoVacuum on
select name, setting, boot_val, reset_val from pg_settings where name like '%vacuum%';
SELECT name, setting FROM pg_settings WHERE name='track_counts';

SELECT * from pg_settings where category like 'Autovacuum';
SELECT * from pg_settings where category like 'Auto%';
--Table specific vacuum settings
SELECT reloptions FROM pg_class WHERE relname like '%api%';

-- Calculate each table's auto-vacuum threshold
SELECT
schemaname, relname, n_tup_ins as "inserts",n_tup_upd as "updates",n_tup_del as "deletes",
n_live_tup as "live_tuples", n_dead_tup::bigint as "dead_tuples",
last_autovacuum, last_vacuum, last_autoanalyze , last_analyze,
(n_tup_ins + n_tup_upd + n_tup_del::bigint + n_live_tup + n_dead_tup)::bigint as TotalTuples,
( n_dead_tup::bigint * (SELECT setting::decimal from pg_settings where name like 'autovacuum_vacuum_scale_factor')
  + (SELECT setting::decimal from pg_settings where name like 'autovacuum_vacuum_threshold')
  ) as VacuumThreshold,
( (n_tup_ins + n_tup_upd + n_tup_del) * (SELECT setting::decimal from pg_settings where name like 'autovacuum_analyze_scale_factor')
  + (SELECT setting::decimal from pg_settings where name like 'autovacuum_analyze_threshold')
  ) as AnalyzeThreshold
FROM pg_stat_user_tables
order by (n_tup_ins + n_tup_upd + n_tup_del + n_live_tup + n_dead_tup)::bigint  desc
                                                                                            
