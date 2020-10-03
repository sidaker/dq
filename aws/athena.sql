SELECT "$path", partition_process_timestamp
FROM api_cross_record_scored_prod.internal_storage_by_std_date_local
where std_date_local = DATE('2020-08-31')
limit 10;

s3://s3-dq-cross-record-scored-prod/internal_storage_by_std_date_local/20201001115050/std_date_local=2020-08-31/partition_process_timestamp=2020-10-01 11%3A50%3A50.0/20201001_115051_00021_cue5h_e7f1722a-fc28-4c77-856b-d00aa2d2e1ee
2020-10-01 11:50:50.000

====================
Convert string to date, custom format

SELECT "$path", partition_process_timestamp
FROM api_cross_record_scored_prod.internal_storage_by_std_date_local
where std_date_local = DATE('2020-08-31')
AND partition_process_timestamp = date_parse('2020-10-01 11:50:50','%Y-%m-%d %H:%i:%s')
limit 10


SELECT count(*)
FROM api_cross_record_scored_prod.internal_storage_by_std_date_local
where std_date_local = DATE('2020-08-30')
AND partition_process_timestamp = date_parse('2020-09-30 11:50:51','%Y-%m-%d %H:%i:%s')

SELECT count(*)
FROM api_cross_record_scored_prod.internal_storage_by_std_date_local
where std_date_local = DATE('2020-08-30')
AND partition_process_timestamp = date_parse('2020-10-01 11:50:50','%Y-%m-%d %H:%i:%s')
