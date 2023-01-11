set deptno=40;
set hiveconf:d1=20;


select * from empty
where col6=${hiveconf:deptno};

set hivevar:deptno=20;

select * from empty
where col6=${hivevar:deptno};


-- hiveconf vs hivevar?
-- Always refer hiveconf with prefix. hiveconf:deptno

hive --hiveconf deptno=20  -f mysql.hql
hive --hivevar deptno=20  -f mysql.hql

set hive.variable.substitute = true;
