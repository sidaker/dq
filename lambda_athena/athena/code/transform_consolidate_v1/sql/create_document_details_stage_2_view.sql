CREATE OR REPLACE VIEW internal_storage_document_details
AS 
      SELECT * FROM internal_storage_document_details_table_history
      UNION ALL
      SELECT * FROM internal_storage_document_details_table_consolidated
      UNION ALL
      SELECT * FROM internal_storage_document_details_table
      WHERE path_name NOT IN ('{path-name-list}')
