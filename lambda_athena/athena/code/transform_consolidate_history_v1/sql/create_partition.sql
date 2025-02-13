CREATE TABLE internal_storage_table_{instance}
WITH (external_location = '{bucket-name}/history/{consolidated-path-name}/',
      format = 'PARQUET',
      parquet_compression = 'SNAPPY')
AS
  SELECT
         *
    FROM
         internal_storage_table_consolidated
   WHERE
         path_name IN ('{path-name-list}')
