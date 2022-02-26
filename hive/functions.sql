select unix_timestamp('2017-04-26 00:00:00');
select YEAR('2017-04-26 00:00:00');
select Month('2017-04-26 00:00:00'); -- 4
select TO_DATE('2017-04-26 00:00:00'); -- 2017-04-26
select HOUR('2017-04-26 00:00:00');
select MINUTE('2017-04-26 00:00:00');
select DAY('2017-04-26 00:00:00');
select SECOND('2017-04-26 00:00:00');
select WEEKOFYEAR('2017-04-26 00:00:00');
select DATEDIFF('2017-04-26 00:00:00', '2017-03-26 00:00:00');
select DATE_ADD('2017-04-26',5)
select DATE_SUB('2017-04-26',5)
----------
select ceil(9.6);
select floor(9.6);
select round(10.5);


select rand();


---------
select concat(col1,':',col3) from tbl;
select length(col3) from tbl;
select lower(col3) from tbl;
select upper(col3) from tbl;
select lpad(col3,9,'v') from tbl;
select rpad(col3,9,'v') from tbl;
select ltrim(col3) from tbl;
select rtrim(col3) from tbl;
select repeat(col3,2) from tbl;
select split(col,'|') from tbl;
select split(col,'|')[0] from tbl;
select substring(col3,4) from tbl;
select substring(col3,4,3) from tbl;
select instr(col3,'e')

---------

select if(col3='xx', col1,col2) from tbl;
select isnull(col1) from tbl;
select isnotnull(col1) from tbl;
select coalesce(col1,col2,col3) from tbl; -- selects first non nulll value.
select NVL(col1,col2) from tbl;

-- Athena
-- SELECT flatten(ARRAY[ ARRAY[1,2], ARRAY[3,4] ]) AS items;

select explode(col2) as c2 from tbl1; -- you cannot include other columns
select explode([1,2,4])

select col1, dummy_col from tbl
lateral view explode(col2) dummy as dummy_col;


-- Separate keys of a map data type column.
select key, value from tbl3 lateral view explode(col1) dummy as key, value

SELECT sample_column FROM sample_data
WHERE sample_column RLIKE '[0-9]+';

SELECT sample_column FROM sample_data
WHERE sample_column RLIKE '^[0-9]+$';

SELECT sample_column FROM sample_data
WHERE sample_column RLIKE '([a-z]|[A-Z])+';

select 'hadoop' rlike 'ha'
select 'hadoop' rlike 'ha*'
select null rlike 'ha'

-- RANK() Vs DENSE_Rank()
-- Ranking done with in ordered partition
select col1, col2, RANK() OVER(ORDER BY col2 desc) from table;
select col1, col2, DENSE_RANK() OVER(ORDER BY col2 desc) from table;
select col1, col2, ROW_NUMBER() OVER(ORDER BY col2 desc) from table;


select col1, col2, RANK() OVER(PARTITION BY col1 ORDER BY col2 desc)
from table;
select col1, col2, DENSE_RANK() OVER(PARTITION BY col1 ORDER BY col2 desc)
from table;
select col1, col2, ROW_NUMBER() OVER(PARTITION BY col1 ORDER BY col2 desc)
from table;

insert into table tbl partition(dt='2022-02-24')
  select * from  tbl2 where dt='2022-02-24'


load data local inpath 'xx/xxx/xx'
into table tbl partition(dt='2022-02-24');

set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;

-- strict vs nonstrict mode

insert into table tbl partition(dt)
select x,y,dt from  tbl2 ;

SHOW PARTITIONS tbl;

ALTER TABLE tbl
DROP PARTITION (dept_name='HR');

ALTER TABLE tbl
ADD PARTITION (dept_name='HR'); --empty partition with no data.

msck repair tbl;

-- How do you arrive at the right number of buckets

set hive.enforce.bucketing = true;

Create table if not exists tbl1
(
  depn int,
  ename string
)
partitioned by (depname string)
clustered by (loction) into 4 buckets
rowformat delimited
fields terminated by ','
lines terminated by '\n';

-- Map Joins are faster on two bucketed tables.
-- Bucketed map joins are fast
-- Both tables should be bucketed on same column and have same number of buckets.

-- sampling
select deptno, ename, local
from dept_tbl
tablesample (bucket 1 out of 2 on location);
-- divides n buckets into 2 buckets and selects data from first bucket
select deptno, ename, local
from dept_tbl
tablesample (2 percent);

select deptno, ename, local
from dept_tbl
tablesample (1M);

select deptno, ename, local
from dept_tbl
tablesample (20 rows);

alter table tbl enable no_drop;
alter table tbl disable no_drop;
alter table tbl enable offline;

alter table tbl partition (dpname='HR')
enable no_drop;

alter table tbl partition (dpname='HR')
enable offline;

alter table tbl partition (dpname='HR')
disable no_drop;

-- by default in joins last table in the query is streamed the rest are in buffer.
-- last table will be streamed through reducers.
-- so always keep the biggest table as the last and let that be streamed and not be kept in memory.
--  Alternatively  mention  it in the query with a hint to let hive know which table would you like to be streamed

select /*+ STREAMTABLE (emp_table) */
emp_table.col1, emp_table.col2,  dept_table.dept_name
from emp_table
join dept_table on
(emp_table.dept_id=dept_table.dept_id)
JOIN third_table ON (third_table.eid=emp_table.eid)

-- what is offline table?

-- Map Joins are faster?
-- In any M/R job, reduce step is the slowest usually as it involves shuffling of data
-- By using map joins you will avoid the reduce step.
-- For Map joins to be performed the pre requisite is one table should be small enough to fit into memory.
-- You can give a query hint to perform map joins.
-- No full outer joins not possible with map joins.
-- Also consider bucketed map joins where possible.


select /*+ MAPJOIN (emp_tab) */
emp_table.col1, emp_table.col2, dept_table.dept_name
from emp_table
join dept_table on
(emp_table.dept_id=dept_table.dept_id);

-- You can also let hive decide
set hive.auto.convert.join=true;
set hive.map.join.smalltable.filesize=2500000


-- bucketed map joins.
set hive.input.format=org.apache.hadoop.hive.ql.io.BucketizedHiveInputFormat
set hive.optimize.bucketmapjoin=true;
set hive.auto.convert.sortmerge.join=true;
set hive.optimize.bucketmapjoin.sortedmerge=true;
