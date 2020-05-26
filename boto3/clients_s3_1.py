import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

s3client = boto3.client('s3',region_name='eu-west-2')

response = s3client.list_buckets()

print(type(response['Buckets']))

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
