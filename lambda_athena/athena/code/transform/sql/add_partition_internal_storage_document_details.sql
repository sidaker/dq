ALTER TABLE internal_storage_document_details_table ADD IF NOT EXISTS
PARTITION (path_name = '{path-name}') LOCATION '{bucket-name}/document_details/{path-name}/';
