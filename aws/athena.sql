SELECT CAST(From_iso8601_timestamp('2018-01-01T15:00:00Z') AS timestamp); -- works.

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

===============

ALTER TABLE orders ADD
  PARTITION (dt = '2016-05-14', country = 'IN') LOCATION 's3://mystorage/path/to/INDIA_14_May_2016/'
  PARTITION (dt = '2016-05-15', country = 'IN') LOCATION 's3://mystorage/path/to/INDIA_15_May_2016/';

  drop_partition_sql = ("ALTER TABLE " + database_name + "." + table_name + \
                             " DROP PARTITION (" + item_quoted + ");")
        add_partition_sql = ("ALTER TABLE " + database_name + "." + table_name + \
                             "_archive ADD PARTITION (" + item_quoted + ") LOCATION 's3://" + s3_location + "/" + item_stripped + "';")

ALTER TABLE bitd_input_test.input_file_bitd_output_unittest
ADD PARTITION "outputfile/"
LOCATION 's3://dq-test-lambda-functions-unittest/outputfile/'


ALTER TABLE internal_storage_table_20201023 ADD IF NOT EXISTS
PARTITION (path_name = '2020-10-23/02:10:54.444767475/')
LOCATION 's3://s3-dq-api-record-level-scoring-prod/2020-10-23/02:10:54.444767475/';


===================

SELECT rank() OVER (
    PARTITION BY voyageid
	ORDER BY update_timestamp desc
   ) rnk
, * FROM "consolidated_schedule_prod"."internal_storage_table_consolidated"
where path_name > '2020-10-01'
and path_name < '2020-10-05'
and voyage_number='2437'
and voyageid in ('KRKSTN20201004FR2437A', 'KRKSTN20201003FR2437A')
order by voyageid, rnk


=============

-- BITD distinct acquired date in a file.
select distinct DATE(SUBSTR(body.DateAcquired, 1, 10)) as dec
from input_file_bitd
where process_date='2020-07-10'
order by dec desc;


-----------------

select CAST(from_iso8601_timestamp(js.isostartdate) AS timestamp)

SELECT CAST(from_iso8601_timestamp(‘2020–04–29 17:00:12’) AS timestamp)


SELECT
CASE
              WHEN DateofBirth IS NULL THEN NULL
              WHEN DateofBirth not like '%-%-%' THEN NULL
              WHEN try_cast(DateofBirth as date) is NULL THEN NULL
              WHEN try_cast(DateofBirth as date) is NULL THEN NULL
              ELSE
              date_parse(DateofBirth,'%Y-%m-%d')
              END AS dob

select
CASE
               WHEN (ExpirationDate IS NULL OR ExpirationDate = '') OR
                    (NOT regexp_like(ExpirationDate, '^((((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[13578]|10|12)([-])(0[1-9]|[12][0-9]|3[01]))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[469]|11)([-])([0][1-9]|[12][0-9]|30))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(02)([-])(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)([-])(02)([-])(29))|(([13579][26]00)([-])(02)([-])(29))|(([0-9][0-9][0][48])([-])(02)([-])(29))|(([0-9][0-9][2468][048])([-])(02)([-])(29))|(([0-9][0-9][13579][26])([-])(02)([-])(29)))$')) OR
                    CAST(ExpirationDate AS VARCHAR(10)) >= CAST(DATE_FORMAT(DATE_PARSE(manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ'), '%Y-%m-%d') AS VARCHAR(10)) THEN 1
               ELSE 0
           END AS df_document_expiration_in_future_score,


  SELECT CAST(DATE_FORMAT(DATE_PARSE(manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ'), '%Y-%m-%d') AS VARCHAR(10))


select   CAST(DATE_FORMAT(DATE_PARSE(A.fs_departuredata_datelocal, '%Y-%m-%dT%H:%i:%s.%f'), '%Y-%m-%d') AS VARCHAR(10)) AS flight_date,
