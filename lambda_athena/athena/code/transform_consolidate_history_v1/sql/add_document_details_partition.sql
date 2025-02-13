ALTER TABLE internal_storage_document_details_table_history ADD IF NOT EXISTS 
PARTITION (path_name = '{consolidated-path-name}') LOCATION '{bucket-name}/document_details/history/{consolidated-path-name}/';

