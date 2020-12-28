SELECT
date_parse((A.departureDate || A.departureTime),'%Y-%m-%d%H:%i:%s') as departuretimelocal


select rank() OVER (PARTITION BY voyageid ORDER BY oag_lastupdated DESC) as rnk , etd, atd, * from "oag_transform_prod"."internal_storage"
 where path_name like '%2020-10-19%'
 and voyageid = 'ISBLHR20201019BA0260A';


 SELECT
       count(voyageid) as total_ct,
       sum(case when atd is NULL then 1 else 0 end) ct_atd_null ,
       sum(case when atd is NOT NULL then 1 else 0 end) ct_atd_valid
 FROM (
 select rank() OVER (PARTITION BY voyageid ORDER BY oag_lastupdated DESC) as rnk , voyageid, atd from "oag_transform_prod"."internal_storage"
 where path_name like '%2020-10-19%' and flight_date IN ( '2020-10-19')) as tb_r
 where tb_r.rnk =  1 ;


 SELECT
        count(voyageid) as total_ct,
        sum(case when atd is NULL then 1 else 0 end) ct_atd_null ,
        sum(case when atd is NOT NULL then 1 else 0 end) ct_atd_valid,
        flight_date
  FROM (
  select rank() OVER (PARTITION BY voyageid ORDER BY oag_lastupdated DESC) as rnk , voyageid, atd, flight_date from "oag_transform_prod"."internal_storage"
  where path_name like '%2020-10-1%' and flight_date IN ( '2020-10-19','2020-10-18','2020-10-17','2020-10-16' )) as tb_r
  where tb_r.rnk =  1
  GROUP BY flight_date
  order by flight_date;


  SELECT distinct path_name FROM "consolidated_schedule_prod"."internal_storage"
  where path_name not like 'bulk%' and path_name not like 'collected/%' and path_name > '2020-10-20'
  order by path_name;


  SELECT
  count(voyageid) as totalct,
  sum(case when atd is NULL then 1 else 0 end) ct_atd_null ,
  sum(case when atd is NOT NULL then 1 else 0 end) ct_atd_valid
  FROM "consolidated_schedule_prod"."internal_storage"
  where path_name not like 'bulk%' and path_name not like 'collected/%' and path_name > '2020-10-21'
  and flight_date = '2020-10-21'
 ---
 Timeliness of each API message will need to re-scored once ATD is known
 from OAG schedule data feed.

 # Aviation Scheduled Status on RDS needs to be re-updated.

 # Update 'api record level score' table with ATDs and Timeliness Delta and scores

 SELECT CAST(date_format(date_parse(SUBSTR('ROPEOXXICEROLL3_20200414.CSV',17,8), '%Y%m%d'), '%Y-%m-%d') AS DATE) AS file_date
-- 2020-04-14
