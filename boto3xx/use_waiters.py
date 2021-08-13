import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='notprod')
S3 = session.client('s3',region_name='eu-west-2')

OUTPUT_BUCKET_NAME="s3://s3-dq-api-arrivals-notprod"
HIGH_WATERMARK_KEY="reference/highwatermark.csv"

S3 = boto3.client('s3')
attempts = 3
i = 1

waiter = S3.get_waiter('object_exists')
waiter.wait(Bucket = OUTPUT_BUCKET_NAME[5:], Key = HIGH_WATERMARK_KEY , WaiterConfig={'Delay': 3,'MaxAttempts': 2})
