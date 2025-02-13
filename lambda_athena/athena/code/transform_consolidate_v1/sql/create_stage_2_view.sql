CREATE OR REPLACE VIEW internal_storage
AS 
      SELECT * FROM internal_storage_table_history
      UNION ALL
      SELECT * FROM internal_storage_table_consolidated
      UNION ALL
      SELECT * FROM internal_storage_table
      WHERE path_name NOT IN ('{path-name-list}')
