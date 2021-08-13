import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# To use resources, you invoke the resource() method of a Session and pass in a service name:
s3 = boto3.resource('s3',region_name='eu-west-2')

# list all buckets in my account


# S3: Wait for a bucket to exist.
#bucket.wait_until_exists()
