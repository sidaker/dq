CREATE TABLE internal_storage_table_{instance}
WITH (external_location = '{bucket-name}/consolidated/{consolidated-path-name}/',
      format = 'PARQUET',
      parquet_compression = 'SNAPPY')
AS
  SELECT
         *
    FROM
         internal_storage_table
   WHERE
         path_name IN ('{path-name-list}')
