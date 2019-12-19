import boto3
from datetime import datetime
from botocore.exceptions import ClientError


def execute_glue_api(DATABASE_NAME,TB_NAME,partition_val):
    client = boto3.client('glue',region_name='eu-west-2')
    try:
        client.delete_partition(DatabaseName=DATABASE_NAME,TableName=TB_NAME,PartitionValues=[partition_val])
    except ClientError as e:
        print('partition not exist',e.response['Error']['Code'])

def lambda_handler(event, context):
    DATABASE_NAME='api_input_notprod'
    TB_NAME='input_file_api'
    partition_val='2019-12-03/12:03:29.036194'
    execute_glue_api(DATABASE_NAME,TB_NAME,partition_val)
    return { 'statusCode': 200 }
