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
