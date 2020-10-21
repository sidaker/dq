import boto3
client = boto3.client('athena', region_name='eu-west-2')
response = client.start_query_execution(QueryString='select * from api_cross_record_scored_notprod.internal_storage_by_std_date_local limit 10',
                                        QueryExecutionContext={'Database': 'api_cross_record_scored_notprod'},
                                        ResultConfiguration={'OutputLocation': 's3://s3-athena-log/'})
query_execution_id = response['QueryExecutionId']
print (query_execution_id)
