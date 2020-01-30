import boto3
import io
import pandas as pd

# Read single parquet file from S3
def pd_read_s3_parquet(key, bucket, s3_client=None, **args):
    if s3_client is None:
        s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(io.BytesIO(obj['Body'].read()), **args)

df = pd_read_s3_parquet('btid/DataFeedId=5/2020-01-27/bx_test_data.snappy.parquet','s3-dq-cdlz-btid-input')
print(type(df))

print(df)
