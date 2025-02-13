CREATE TABLE internal_storage_document_details_table_{instance}
WITH (external_location = '{bucket-name}/document_details/consolidated/{consolidated-path-name}/',
      format = 'PARQUET',
      parquet_compression = 'SNAPPY')
AS
  SELECT
         *
    FROM
         internal_storage_document_details_table
   WHERE
         path_name IN ('{path-name-list}')
