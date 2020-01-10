aws athena start-query-execution \
--query-string "ALTER TABLE api_cross_record_scored_notprod.internal_storage_by_std_date_local SET LOCATION 's3://s3-dq-cross-record-scored-notprod/internal_storage_by_std_date_local/';" \
--result-configuration "OutputLocation"="s3://s3-dq-athena-log-notprod" --region "eu-west-2"  \
--profile notprod

aws athena get-query-execution \
--region "eu-west-2"  \
--query-execution-id "23b28b3e-33c2-47ad-85a6-bbdd5b1281aa" --profile notprod
