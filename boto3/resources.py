import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa

'''
Every resource instance has a number of attributes and methods.
These can conceptually be split up into
identifiers, attributes, actions, references, sub-resources, and collections.
'''
# Get resources from the default session
sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')

# SQS Queue (url is an identifier)
# queue = sqs.Queue(url='http://...')
# print(queue.url)

# S3 Object (bucket_name and key are identifiers)
obj = s3.Object(bucket_name='s3-dq-cdlz-btid-input', key='btid/DataFeedId=5/2020-01-27/bx_test_data.snappy.parquet')
print(obj.bucket_name)
print(obj.key)

# Raises exception, missing identifier: key!
try:
    obj = s3.Object(bucket_name='boto3')
except Exception as e:
    print(e)


# Identifiers may also be passed as positional arguments:
# S3 Object
obj_positional = s3.Object('s3-dq-cdlz-btid-input', 'btid/DataFeedId=5/2020-01-27/bx_test_data.snappy.parquet')
# Resources may also have attributes, which are lazy-loaded properties on the instance.
print(obj_positional.last_modified)
print(obj_positional.e_tag)

# S3 Object
response = obj.get()
parquetdata = response['Body'].read()
# read parquet file.

'''
parquet_file1 = pq.ParquetFile('bx_test_data_noindex.parquet')
print("Print metadata")
print(parquet_file1.metadata)
print(parquet_file1.schema)
'''
