import boto3
import io
import pandas as pd
from botocore.config import Config
from botocore.exceptions import ClientError


# Read single parquet file from S3
def pd_read_s3_parquet(key, bucket, s3_client=None, **args):
    if s3_client is None:
        s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(io.BytesIO(obj['Body'].read()), **args)

session = boto3.Session(profile_name='prod')
s3client = session.client('s3',region_name='eu-west-2')
df = pd_read_s3_parquet('s3://s3-dq-cdlz-bitd-input-prod/bitd/2020-04-30/06:15:56.746706/part-00000-cb0dcd2b-ec53-4eee-9a74-7db60a708cc1-c000.snappy.parquet','s3-dq-cdlz-bitd-input-prod')
print(type(df))

print(df)
