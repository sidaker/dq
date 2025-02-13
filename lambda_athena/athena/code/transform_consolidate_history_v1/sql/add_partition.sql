ALTER TABLE internal_storage_table_history ADD IF NOT EXISTS 
PARTITION (path_name = '{consolidated-path-name}') LOCATION '{bucket-name}/history/{consolidated-path-name}/';
