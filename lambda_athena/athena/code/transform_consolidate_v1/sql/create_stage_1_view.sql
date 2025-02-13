CREATE OR REPLACE VIEW internal_storage
AS 
      SELECT * FROM internal_storage_table_history
      UNION ALL
      SELECT * FROM internal_storage_table_consolidated
      WHERE path_name <> '{consolidated-path-name}'
      UNION ALL
      SELECT * FROM internal_storage_table
