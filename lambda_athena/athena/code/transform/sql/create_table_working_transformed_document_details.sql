#pre_execution_pause_seconds:10
CREATE TABLE api_working_transformed_document_details_{instance}
WITH (external_location = '{bucket-name}/document_details/{path-name}/',
      format = 'PARQUET',
      parquet_compression = 'SNAPPY')
AS
SELECT
    passengerDetails_DocumentDetails_documentType,
    passengerDetails_DocumentDetails_documentNo,
    passengerDetails_DocumentDetails_docIssueDate,
    passengerDetails_DocumentDetails_docExpirationDate,
    passengerDetails_DocumentDetails_countryOfIssue,
    passengerDetails_DocumentDetails_cityOfIssue,
    doc_type_md_code,
    doc_type_level,
    doc_type_Row_Number,
    cf_document_country_of_issue_not_blank_score,
    cf_Document_expiration_not_blank_score,
    cf_document_number_not_blank_score,
    cf_document_type_not_blank_score,
    df_document_expiration_in_future_score,
    df_document_issuing_country_refdata_match_score,
    df_document_number_length_score,
    df_document_type_refdata_match_score,
    vf_document_expiration_is_date_score,
    vf_document_issuing_country_length_score,
    vf_document_issuing_country_char_score,
    vf_document_number_length_score,
    vf_document_number_alphanumeric_score,
    hub_parsed_message_sqn,
    hub_document_sqn,
    id,
    s3_location,
    xml_file_name,
    file_name,
    vf_document_type_length_score,
    vf_document_type_char_score
FROM
    (
    SELECT
        passengerDetails_DocumentDetails_documentType,
        passengerDetails_DocumentDetails_documentNo,
        passengerDetails_DocumentDetails_docIssueDate,
        passengerDetails_DocumentDetails_docExpirationDate,
        passengerDetails_DocumentDetails_countryOfIssue,
        passengerDetails_DocumentDetails_cityOfIssue,
        doc_type_md_code,
        doc_type_level,
        ROW_NUMBER() OVER(PARTITION BY hub_parsed_message_sqn ORDER BY (DocumentDetails_Row_Num,passengerDetails_DocumentDetails_documentNo)) AS doc_type_Row_Number,
        cf_document_country_of_issue_not_blank_score,
        cf_Document_expiration_not_blank_score,
        cf_document_number_not_blank_score,
        cf_document_type_not_blank_score,
        df_document_expiration_in_future_score,
        df_document_issuing_country_refdata_match_score,
        df_document_number_length_score,
        df_document_type_refdata_match_score,
        vf_document_expiration_is_date_score,
        vf_document_issuing_country_length_score,
        vf_document_issuing_country_char_score,
        vf_document_number_length_score,
        vf_document_number_alphanumeric_score,
        hub_parsed_message_sqn,
        hub_document_sqn,
        hub_document_sqn AS id,
        s3_location,
        xml_file_name,
        file_name,
	vf_document_type_length_score,
	vf_document_type_char_score,
        ROW_NUMBER() OVER(PARTITION BY hub_document_sqn ORDER BY hub_document_sqn) AS rnum
    FROM
        (
        SELECT
            passengerDetails_DocumentDetails_documentType,
            passengerDetails_DocumentDetails_documentNo,
            passengerDetails_DocumentDetails_docIssueDate,
            passengerDetails_DocumentDetails_docExpirationDate,
            passengerDetails_DocumentDetails_countryOfIssue,
            passengerDetails_DocumentDetails_cityOfIssue,
            dt.md_code AS doc_type_md_code,
            dt.doctype_level AS doc_type_level,
            TO_HEX(MD5(TO_UTF8(UPPER(TRIM(xml_file_name))))) AS hub_parsed_message_sqn,
            TO_HEX(MD5(TO_UTF8(UPPER(TRIM(passengerDetails_DocumentDetails_documentNo))||UPPER(TRIM(xml_file_name))||UPPER(TRIM(passengerDetails_DocumentDetails_documentType))||UPPER(TRIM(passengerDetails_DocumentDetails_countryOfIssue))))) AS hub_document_sqn,
            CASE passengerDetails_DocumentDetails_documentType
                                                      WHEN 'P' THEN 1
                                                      WHEN 'PASSPORT' THEN 1
                                                      WHEN 'D' THEN 2
                                                      WHEN 'DIPLOMATIC IDENTIFICATION' THEN 2
                                                      WHEN 'G' THEN 3
                                                      WHEN 'GROUP PASSPORT' THEN 3
                                                      WHEN 'IDENTITYCARD' THEN 4
                                                      WHEN 'IDENTITY CARD' THEN 4
                                                      WHEN 'A' THEN 5
                                                      WHEN 'C' THEN 6
                                                      WHEN 'I' THEN 7
                                                      WHEN 'M' THEN 8
                                                      WHEN 'MILITARY IDENTIFICATION' THEN 8
                                                      WHEN 'F' THEN 9
                                                      WHEN 'OTHER' THEN 9
                                                      WHEN 'V' THEN 10
                                                      WHEN 'IP' THEN 11
                                                      WHEN 'PASSPORT CARD' THEN 11
                                                      WHEN 'AC' THEN 12
                                                      WHEN 'CREW MEMBER CERTIFICATE' THEN 12
                                                      ELSE 13
                                                      END AS DocumentDetails_Row_Num,
            --Field Level Completeness - CF
            CASE
                WHEN passengerDetails_DocumentDetails_countryOfIssue IS NOT NULL AND passengerDetails_DocumentDetails_countryOfIssue <> '' THEN 1
                ELSE 0
            END AS cf_document_country_of_issue_not_blank_score,
            CASE
                WHEN passengerDetails_DocumentDetails_docExpirationDate IS NOT NULL AND passengerDetails_DocumentDetails_docExpirationDate <> '' THEN 1
                ELSE 0
            END AS cf_Document_expiration_not_blank_score,
            CASE
                WHEN passengerDetails_DocumentDetails_documentNo IS NOT NULL AND passengerDetails_DocumentDetails_documentNo <> '' THEN 1
                ELSE 0
            END AS cf_document_number_not_blank_score,
            CASE
                WHEN passengerDetails_DocumentDetails_documentType IS NOT NULL AND passengerDetails_DocumentDetails_documentType <> '' THEN 1
                ELSE 0
            END AS cf_document_type_not_blank_score,
            --Field Level Definition - DF
            CASE
                WHEN (passengerDetails_DocumentDetails_docExpirationDate IS NULL OR passengerDetails_DocumentDetails_docExpirationDate = '') OR
                     (NOT regexp_like(passengerDetails_DocumentDetails_docExpirationDate, '^((((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[13578]|10|12)([-])(0[1-9]|[12][0-9]|3[01]))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[469]|11)([-])([0][1-9]|[12][0-9]|30))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(02)([-])(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)([-])(02)([-])(29))|(([13579][26]00)([-])(02)([-])(29))|(([0-9][0-9][0][48])([-])(02)([-])(29))|(([0-9][0-9][2468][048])([-])(02)([-])(29))|(([0-9][0-9][13579][26])([-])(02)([-])(29)))$')) OR
                     CAST(passengerDetails_DocumentDetails_docExpirationDate AS VARCHAR(10)) >= CAST(DATE_FORMAT(DATE_PARSE(manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ'), '%Y-%m-%d') AS VARCHAR(10)) THEN 1
                ELSE 0
            END AS df_document_expiration_in_future_score,
            CASE
                WHEN (passengerDetails_DocumentDetails_countryOfIssue IS NULL OR passengerDetails_DocumentDetails_countryOfIssue = '') OR
                      con.country_md_code IS NOT NULL THEN 1
                ELSE 0
            END AS df_document_issuing_country_refdata_match_score,
            CASE
                WHEN (passengerDetails_DocumentDetails_documentNo IS NULL OR passengerDetails_DocumentDetails_documentNo = '') OR
                      LENGTH(passengerDetails_DocumentDetails_documentNo) >= 5 THEN 1
                ELSE 0
            END AS df_document_number_length_score,
            CASE
                WHEN (passengerDetails_DocumentDetails_documentType IS NULL OR passengerDetails_DocumentDetails_documentType = '') OR
                      dt.md_code IS NOT NULL THEN 1
                ELSE 0
            END AS df_document_type_refdata_match_score,
            --Field Level Validity - VF
            CASE
                WHEN (passengerDetails_DocumentDetails_docExpirationDate IS NULL OR passengerDetails_DocumentDetails_docExpirationDate = '') OR
                      regexp_like(passengerDetails_DocumentDetails_docExpirationDate, '^((((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[13578]|10|12)([-])(0[1-9]|[12][0-9]|3[01]))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[469]|11)([-])([0][1-9]|[12][0-9]|30))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(02)([-])(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)([-])(02)([-])(29))|(([13579][26]00)([-])(02)([-])(29))|(([0-9][0-9][0][48])([-])(02)([-])(29))|(([0-9][0-9][2468][048])([-])(02)([-])(29))|(([0-9][0-9][13579][26])([-])(02)([-])(29)))$') THEN 1
                ELSE 0
            END AS vf_document_expiration_is_date_score,
            CASE
                WHEN (passengerDetails_DocumentDetails_countryOfIssue IS NULL OR passengerDetails_DocumentDetails_countryOfIssue = '') OR
                      LENGTH(passengerDetails_DocumentDetails_countryOfIssue) = 3 THEN 1
                ELSE 0
            END AS vf_document_issuing_country_length_score,
            CASE
                WHEN (passengerDetails_DocumentDetails_countryOfIssue IS NULL OR passengerDetails_DocumentDetails_countryOfIssue = '') OR
                      regexp_like(passengerDetails_DocumentDetails_countryOfIssue, '^[a-zA-Z]+$') THEN 1
                ELSE 0
            END AS vf_document_issuing_country_char_score,
            CASE
                WHEN (passengerDetails_DocumentDetails_documentNo IS NULL OR passengerDetails_DocumentDetails_documentNo = '') OR
                      LENGTH(TRIM(passengerDetails_DocumentDetails_documentNo)) BETWEEN 1 AND 35 THEN 1
                ELSE 0
            END AS vf_document_number_length_score,
            CASE
                WHEN (passengerDetails_DocumentDetails_documentNo IS NULL OR passengerDetails_DocumentDetails_documentNo = '') OR
                      regexp_like(passengerDetails_DocumentDetails_documentNo, '^[0-9a-zA-Z]+$') THEN 1
                ELSE 0
            END AS vf_document_number_alphanumeric_score,
            s3_location,
            xml_file_name,
            file_name,
            CASE
                WHEN (passengerDetails_DocumentDetails_documentType IS NULL OR passengerDetails_DocumentDetails_documentType = '') OR
                      LENGTH(passengerDetails_DocumentDetails_documentType) <= 3 THEN 1
                ELSE 0
            END AS vf_document_type_length_score,
            CASE
                WHEN (passengerDetails_DocumentDetails_documentType IS NULL OR passengerDetails_DocumentDetails_documentType = '') OR
                      regexp_like(passengerDetails_DocumentDetails_documentType, '^[a-zA-Z]+$') THEN 1
                ELSE 0
            END AS vf_document_type_char_score
        FROM
            api_input_{namespace}.input_file_api api
            LEFT OUTER JOIN reference_data_{namespace}.ref_doc_type dt ON UPPER(passengerDetails_DocumentDetails_documentType) = dt.md_code
            LEFT OUTER JOIN reference_data_{namespace}.countries con ON UPPER(passengerDetails_DocumentDetails_countryOfIssue) = con.country_md_code
        WHERE
            api.path_name = '{path-name}'
            AND api.extra_rec_type IN ('main','documentdetails')
        )api
    )api
where
  rnum = 1;
