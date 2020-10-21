EXPLAIN select * from staff
 -- "Seq Scan on staff  (cost=0.00..24.00 rows=1000 width=75)"

EXPLAIN select * from staff
where id<300
-- "Index Scan using staff_pkey on staff  (cost=0.28..21.52 rows=299 width=75)"
-- "  Index Cond: (id < 300)"

EXPLAIN ANALYZE select last_name from staff
where id<300
-- "Index Scan using staff_pkey on staff  (cost=0.28..21.52 rows=299 width=7) (actual time=0.064..0.230 rows=299 loops=1)"
-- "  Index Cond: (id < 300)"
-- "Planning Time: 0.073 ms"
-- "Execution Time: 1.653 ms"


EXPLAIN select
s.id, s.last_name, s.job_title, cr.country
FROM Staff s
INNER JOIN company_regions cr
ON s.region_id = cr.region_id;

"Hash Join  (cost=22.38..49.02 rows=1000 width=88)"
"  Hash Cond: (s.region_id = cr.region_id)"
"  ->  Seq Scan on staff s  (cost=0.00..24.00 rows=1000 width=34)"
"  ->  Hash  (cost=15.50..15.50 rows=550 width=62)"
"        ->  Seq Scan on company_regions cr  (cost=0.00..15.50 rows=550 width=62)"

Query Builder determined a hash join is most effective for this.

Can we force the Query builder to use a Nested loop join? Yes.

set enable_nestloop = true;
set enable_hashjoin = false;
set enable_mergejoin = false;

EXPLAIN select
s.id, s.last_name, s.job_title, cr.country
FROM Staff s
INNER JOIN company_regions cr
ON s.region_id = cr.region_id;

"Nested Loop  (cost=0.15..239.37 rows=1000 width=88)"
"  ->  Seq Scan on staff s  (cost=0.00..24.00 rows=1000 width=34)"
"  ->  Index Scan using company_regions_pkey on company_regions cr  (cost=0.15..0.22 rows=1 width=62)"
"        Index Cond: (region_id = s.region_id)"
