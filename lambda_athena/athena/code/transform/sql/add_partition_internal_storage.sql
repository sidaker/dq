ALTER TABLE internal_storage_table ADD IF NOT EXISTS
PARTITION (path_name = '{path-name}') LOCATION '{bucket-name}/{path-name}/';
