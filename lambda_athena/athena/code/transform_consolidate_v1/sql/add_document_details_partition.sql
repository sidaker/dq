ALTER TABLE internal_storage_document_details_table_consolidated ADD IF NOT EXISTS
PARTITION (path_name = '{consolidated-path-name}') LOCATION '{bucket-name}/document_details/consolidated/{consolidated-path-name}/';
