import boto3
env='notprod'
session = boto3.Session(profile_name=env)
client = session.client('athena', region_name='eu-west-2')

response = client.start_query_execution(QueryString='select * from api_cross_record_scored_notprod.internal_storage_by_std_date_local limit 10',
                                        QueryExecutionContext={'Database': 'api_cross_record_scored_notprod'},
                                        WorkGroup= "primary",
                                        ResultConfiguration={'OutputLocation': 's3://s3-dq-athena-log-notprod'})
query_execution_id = response['QueryExecutionId']
print (query_execution_id)
