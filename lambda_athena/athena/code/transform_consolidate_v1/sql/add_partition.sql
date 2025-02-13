ALTER TABLE internal_storage_table_consolidated ADD IF NOT EXISTS
PARTITION (path_name = '{consolidated-path-name}') LOCATION '{bucket-name}/consolidated/{consolidated-path-name}/';
