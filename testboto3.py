import boto3
import os
from boto3.session import Session

# SHOW TABLES IN asn_maritime_test 'internal_storage_table_*_20210708*'
# Change the profile of the default session in code
env='dqtest'
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
session = boto3.Session(profile_name=env)
#session = boto3.Session()
s3 = session.client('s3')
