import boto3
import logging
import os
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('glue')
s3 = boto3.resource('s3')

# This lambda is used to get the status of the Glue Cralwer
def lambda_handler(event, context):
  
    sfClient = boto3.client('stepfunctions', region_name = 'eu-west-1')
    # bucket = 'sdlf-lubes-921380586770-artifacts'
    # key = 'jdechina-historical-pipeline/jdechina_historical_full_load.json'
    
    bucketName = os.environ.get('BUCKETNAME')
    awsAccountId = os.environ.get('ACCOUNTID')
    region = os.environ.get('REGION')
    pipelineName = os.environ.get('PIPELINE')
    
    sfInputFileName = event['sfInputFileName']
    stepFunctionName = event['sfName']
    
    key = f'{pipelineName}/{sfInputFileName}'
    sfArn = f'arn:aws:states:{region}:{awsAccountId}:stateMachine:{stepFunctionName}'
    
    obj = s3.Object(bucketName, key)
    data = obj.get()['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    
    response = sfClient.start_execution(
                      stateMachineArn = sfArn,
                      input = json.dumps(json_data)
                )
    
    return 1
