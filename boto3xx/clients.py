import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='notprod')
sqsclient = session.client('sqs',region_name='eu-west-2')
s3client = session.client('s3',region_name='eu-west-2')
