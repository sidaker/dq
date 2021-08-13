# GetWorkGroup
import boto3
env='notprod'
session = boto3.Session(profile_name=env)
client = session.client('athena', region_name='eu-west-2')

response = client.get_work_group(
    WorkGroup='primary'
)
print(response.keys())
print(response.values())
print(response['WorkGroup']['Configuration']['EngineVersion'])
print(response['ResponseMetadata'])
