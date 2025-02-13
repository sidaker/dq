CREATE EXTERNAL TABLE IF NOT EXISTS internal_storage_document_details_table
(
    passengerDetails_DocumentDetails_documentType VARCHAR(200),
    passengerDetails_DocumentDetails_documentNo VARCHAR(200),
    passengerDetails_DocumentDetails_docIssueDate VARCHAR(200),
    passengerDetails_DocumentDetails_docExpirationDate VARCHAR(200),
    passengerDetails_DocumentDetails_countryOfIssue VARCHAR(200),
    passengerDetails_DocumentDetails_cityOfIssue VARCHAR(200),
    doc_type_md_code VARCHAR(100),
    doc_type_level VARCHAR(100),
    doc_type_Row_Number INTEGER,
    cf_document_country_of_issue_not_blank_score INTEGER,
    cf_Document_expiration_not_blank_score INTEGER,
    cf_document_number_not_blank_score INTEGER,
    cf_document_type_not_blank_score INTEGER,
    df_document_expiration_in_future_score INTEGER,
    df_document_issuing_country_refdata_match_score INTEGER,
    df_document_number_length_score INTEGER,
    df_document_type_refdata_match_score INTEGER,
    vf_document_expiration_is_date_score INTEGER,
    vf_document_issuing_country_length_score INTEGER,
    vf_document_issuing_country_char_score INTEGER,
    vf_document_number_length_score INTEGER,
    vf_document_number_alphanumeric_score INTEGER,
    hub_parsed_message_sqn VARCHAR(100),
    hub_document_sqn VARCHAR(100),
    id VARCHAR(100),
    s3_location VARCHAR(1000),
    xml_file_name VARCHAR(250),
    file_name VARCHAR(250),
    vf_document_type_length_score INTEGER,
    vf_document_type_char_score INTEGER
)
PARTITIONED BY (path_name STRING)
STORED AS PARQUET
LOCATION '{bucket-name}/exclude/{path-name}/';
