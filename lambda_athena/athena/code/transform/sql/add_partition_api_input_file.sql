ALTER TABLE api_input_{namespace}.input_file_api ADD IF NOT EXISTS
PARTITION (path_name = '{path-name}') LOCATION '{input-bucket-name}/{path-name}/';
