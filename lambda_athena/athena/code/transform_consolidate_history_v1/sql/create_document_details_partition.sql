CREATE TABLE internal_storage_document_details_table_{instance}
WITH (external_location = '{bucket-name}/document_details/history/{consolidated-path-name}/',
      format = 'PARQUET',
      parquet_compression = 'SNAPPY')
AS
  SELECT
         *
    FROM
         internal_storage_document_details_table_consolidated
   WHERE
         path_name IN ('{path-name-list}')

