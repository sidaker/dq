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


show tables;
-- partitions at HDFS level and Indexing at Table level.

create index indx1 on table1(col3) as 'COMPACT'
with deferred rebuild;
alter index indx1 on table1 rebuild;
-- index table will be refreshed when you run above

create index indx1 on table1(col3) as 'COMPACT'
with deferred rebuild stored as rcfile;

create index indx1 on table1(col3) as 'COMPACT'
with deferred rebuild
rowformat delimited field
fields terminated by '\n'
stored as textfile ;

create index indx2 on table1(col3) as 'BITMAP'
with deferred rebuild;
alter index indx2 on table1 rebuild;

show formatted indexes on tbl1;

drop index i1 on tbl1;

-- Compact vs Bitmap indexes.

-- STEPS to Create UDF's
1. Write a Java Program
2. Convert into JAR.
3. Add the JAR file to hive.
4. Create the function of the JAR file added.
5. Use the function in Hive Query

Join optimizations
- By reducing the amount of data held in memory.
- By Map joins thus eliminating the reduce phase.

One table is held in memory(smaller table for better perf) while the other is read
record by record from disk.

When Partitioning
ensure the partition key does not heavily skew the data.

Partition - directory in HDFS
Bucket - a file in HDFS

Bucketing helps in
- Joins (Map Joins)
- Faster joins when two tables are bucketed on same column and have same no of buckets.
- Sampling (Selecting from specific buckets)

The JAR you need to run a UDF:
hive-exec-0.14.0.jar

Create a Java Project with all dependencies.
Create a new Java Package and a Java Class inside it.
Create a JAR file.
add jar <>
-- add jar file to class path
create temporary function f2 as 'com.hive1.myud2'

import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

public final class myud2 extends UDF{
       public Text evaluate(final Text s)
       {
       if(s==null)
       {
          return null;
       }
          return new Text(s.toString().toUpperCase());

       }
}


-- Table Properties
"skip.header.line.count"="3"
"skip.footer.line.count"="3"
"immutable"="true"
"auto.purge"="true"
"serialization.null.format=""
"transactional"="true"

load data localinpath '/xx/xx' into table t2;

-- insert new data into  an existing partition with out overwriting existing data
-- When the table is mutable this is possible and post insert into table 1 will have additional data from tabl2
insert into table table1
select * from table2;
-- if table 1 is declared as immutable then inserting into a non-empty immutable table is not allowed.

insert overwrite table tbl3
select * from tbl2;
-- inserts even if tbl3 is immutable but now it will have contents only from tbl2

-- if you use purge, when dropping an internal table data will not go to Trash but will be permanently deleted.

Is Transaction features still supported only for
-  ORC.
- Bucketed tables.
-  Are Begin, Commit and Rollback features supported?
- Allowed only with in a session where transactional properties are set.

""

ORC File format properties.
"orc.compress"="zlib"
"orc.compress.size"="value"
"orc.stripe.size"="value"
"orc.row.index.stride"="value"
"orc.create.index"="true"
"orc.bloom.filter.columns"
"orc.bloom.filter.fpp"
