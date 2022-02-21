import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import time
import json

env='notprod'
session = boto3.Session(profile_name=env)
new_event = {}
new_event['Records'] = [{}]
new_event['Records'][0]['ATHENA_OPERATION'] = 'ADDPART'
new_event['Records'][0]['OUTPUT_BUCKET_NAME'] = 's3-dq-cdlz-bitd-input-notprod'
new_event['Records'][0]['TABLE_NAME'] = 'input_file_bitd'
new_event['Records'][0]['DATABASE_NAME'] = 'bitd_input_notprod'
new_event['Records'][0]['TARGET_PATH_NAME'] = 'bitd/'
new_event['Records'][0]['PART_PATH'] = 's3://s3-dq-cdlz-bitd-input-notprod/bitd/2022-01-28/16:08:21.499751/'
new_event['Records'][0]['PROCESS_DATE'] = '2022-01-28'
new_event['Records'][0]['PROCESS_TIME'] = '16:08:21.499751'

'''
{'Records': [{'ATHENA_OPERATION': 'ADDPART', 'OUTPUT_BUCKET_NAME': 's3-dq-cdlz-bitd-input-prod',
'TABLE_NAME': 'input_file_bitd', 'DATABASE_NAME': 'bitd_input_prod',
'TARGET_PATH_NAME': 'bitd/', 'PART_PATH': 's3://s3-dq-cdlz-bitd-input-prod/bitd/2022-02-08/07:05:31.536913/',
 'PROCESS_DATE': '2022-02-08', 'PROCESS_TIME': '07:05:31.536913'}]}
'''

# arn:aws:lambda:eu-west-2:797728447925:function:bitd-input-notprod-lambda
# arn:aws:lambda:eu-west-2:483846886818:function:bitd-input-notprod-lambda-rds
CONFIG = Config(
    retries=dict(
        max_attempts=20
    )
)

state_machine_name = 'bitd-input-notprod-add-partitions'
account_id = '483846886818'
client = session.client('stepfunctions', config=CONFIG, region_name='eu-west-2')

response = client.start_execution(
stateMachineArn=(
    'arn:aws:states:eu-west-2:{0}:stateMachine:{1}'.format(
    account_id,
    state_machine_name)),
    input=json.dumps(new_event))

print(response)
