import boto3
import csv
import os

env='notprod'
dbname='api_record_level_score_notprod'
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
session = boto3.Session(profile_name=env)
aclient = session.client('athena', region_name='eu-west-2')

query_execution_id='9685b19f-7757-4428-accb-1659941dcd8e'

resp = aclient.get_query_execution(QueryExecutionId=query_execution_id)

print(resp['QueryExecution']['Status']['State'])
print(resp)

# s3://s3-dq-athena-log-notprod/00000960-761f-48a3-9ca1-5182f78e37b5.txt
