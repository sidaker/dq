
import os
import sys
import time
import random
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import csv
import json
import re
import urllib.request
import boto3
from dateutil.relativedelta import relativedelta
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
'''
SELECT * FROM "bitd_input_test"."input_file_bitd_output_unittest" limit 10;

path_name=outputfile/

SHOW PARTITIONS input_file_bitd_output_unittest

ALTER TABLE bitd_input_test.input_file_bitd_output_unittest
ADD PARTITION(path_name="2020-08-01/180019")
LOCATION 's3://dq-test-lambda-functions-unittest/outputfile/';
'''

def condition(dic,retention):
    ''' Define your own condition here'''
    match = PATTERN.search(dic['Values'][0]).group(0)
    print(match)
    return dic['Values'][0] < str(retention)

def create_partition(partlist, database_name, table_name):
    """
    Function that calls glue's batch create partition API.
    """
    print("Creating:", partlist)
    create_partition_response = GLUE.batch_create_partition(
            DatabaseName=database_name,
            TableName=table_name,
            PartitionInputList=partlist
        )


def execute_glue_api_delete(database_name, tb_name, partition_val):
    """
    Function that calls glue's batch delete partition API.
    """
    try:

        GLUE.batch_delete_partition(DatabaseName=database_name, TableName=tb_name, PartitionsToDelete=partition_val)
        print("Dropped:", partition_val)
    except ClientError as err:
        if err.response['Error']['Code'] in 'EntityNotFoundException':
            err = 'Table ' + database_name + '.' + tb_name + ' partitions'  + ' not found!'
            LOGGER.warning(err)
            print(err)
        else:
            LOGGER.error(err)


def get_partitions(database, table):
    """
    Loop until the query is either successful or fails
    Args:
        database, table      : the submitted query execution id
    Returns:
        A list of partitions
    """
    try:
        #gluesession = boto3.Session(profile_name='prod')
        #glue_client = gluesession.client("glue", "eu-west-2")

        kwargs = {
            'DatabaseName' : database,
            'TableName' : table,
            'MaxResults' : 25,
            }

        while True:
            resp = GLUE.get_partitions(**kwargs)
            print(resp)
            listb = [{'Values': d['Values']} for d in resp['Partitions'] ]

            x = [[]]
            for idx,val in enumerate(listb):
                 x[0].append(val)

            yield from x
            try:
                kwargs['NextToken'] = resp['NextToken']
            except KeyError as err:
                break
    except Exception as err:
        print(err)


if __name__=='__main__':
    # Change the profile of the default session in code
    PATTERN = re.compile("20[0-9]{2}-[0-9]{1,2}-[0-9]{1,2}")
    TWOMONTHSPLUSCURRENT = ((datetime.date.today() - relativedelta(months=2)).replace(day=1) - datetime.timedelta(days=1))
    THIRTYDAYS = (datetime.date.today() - datetime.timedelta(days=30))
    TODAY = datetime.date.today()

    boto3.setup_default_session(profile_name='default')
    database_name='bitd_input_test'
    table_name='input_file_bitd_output_unittest'
    retention = str(THIRTYDAYS)

    CONFIG = Config(
        retries=dict(
            max_attempts=10
        )
    )

    GLUE = boto3.client('glue', config=CONFIG , region_name='eu-west-2')



    # yields 25 partition at a time
    for parts in get_partitions(database_name, table_name):
        print(parts)
        print(len(parts)) # max 25
        # Apply filter.
        filtered2 = [newparts for newparts in parts if condition(newparts,THIRTYDAYS)]
        print(filtered2)
        print(len(filtered2))
        #create_partition(parts, database_name, f'{table_name}_archive')
        #execute_glue_api_delete(database_name, table_name, parts)

        #newparts = list(filter(lambda d: d['Values'] in keyValList, parts))
        #newparts = list(filter(lambda d: False if d['Values'] in '2020-08-04/180019' else True , parts))
        #print(newparts)
        break
        # lambda x: True if x % 2 == 0 else False
        #match = PATTERN.search(vals).group(0)
        #PATTERN.search
        # selected_files = list(filter(regex.search, files))
        # Use filter to implement retention


'''
{'Partitions': [{'Values': ['outputfile/'], 'DatabaseName': 'bitd_input_test', 'TableName': 'input_file_bitd_output_unittest', 'CreationTime': datetime.datetime(2020, 5, 12, 15, 6, 1, tzinfo=tzlocal()), 'StorageDescriptor': {'Columns': [{'Name': 'dateacquired', 'Type': 'string'}, {'Name': 'dateofbirth', 'Type': 'string'}, {'Name': 'deviceid', 'Type': 'string'}, {'Name': 'documentnumber', 'Type': 'string'}, {'Name': 'documenttype', 'Type': 'string'}, {'Name': 'expirationdate', 'Type': 'string'}, {'Name': 'forename', 'Type': 'string'}, {'Name': 'issuingstate', 'Type': 'string'}, {'Name': 'locationid', 'Type': 'string'}, {'Name': 'nationality', 'Type': 'string'}, {'Name': 'platformtype', 'Type': 'string'}, {'Name': 'recordid', 'Type': 'string'}, {'Name': 'sex', 'Type': 'string'}, {'Name': 'surname', 'Type': 'string'}, {'Name': 'traveldirection', 'Type': 'string'}], 'Location': 's3://dq-test-lambda-functions-unittest/outputfile/', 'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat', 'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat', 'Compressed': False, 'NumberOfBuckets': -1, 'SerdeInfo': {'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe', 'Parameters': {'serialization.format': '1'}}, 'BucketColumns': [], 'SortColumns': [], 'Parameters': {}, 'SkewedInfo': {'SkewedColumnNames': [], 'SkewedColumnValues': [], 'SkewedColumnValueLocationMaps': {}}, 'StoredAsSubDirectories': False}, 'CatalogId': '797728447925'}], 'NextToken': 'eyJsYXN0RXZhbHVhdGVkS2V5Ijp7IkhBU0hfS0VZIjp7InMiOiJwLjJhMzU4ZWVkYzUzNzQ5ZmU5MzlkZjUwMmUzNmM1MjVjLjgifSwiUkFOR0VfS0VZIjp7InMiOiJvdXRwdXRmaWxlLyJ9fSwiZXhwaXJhdGlvbiI6eyJzZWNvbmRzIjoxNjAyNzg5NzQxLCJuYW5vcyI6NDE0MDAwMDAwfX0=', 'ResponseMetadata': {'RequestId': '8c04aa85-4879-4ddc-82b9-42b56fb7d0fc', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Wed, 14 Oct 2020 19:22:21 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '1607', 'connection': 'keep-alive', 'x-amzn-requestid': '8c04aa85-4879-4ddc-82b9-42b56fb7d0fc'}, 'RetryAttempts': 0}}
[{'Values': ['outputfile/']}]
1
[Finished in 0.908s]

CREATE EXTERNAL TABLE `input_file_bitd_output_unittest_archive`(
  `dateacquired` string,
  `dateofbirth` string,
  `deviceid` string,
  `documentnumber` string,
  `documenttype` string,
  `expirationdate` string,
  `forename` string,
  `issuingstate` string,
  `locationid` string,
  `nationality` string,
  `platformtype` string,
  `recordid` string,
  `sex` string,
  `surname` string,
  `traveldirection` string)
PARTITIONED BY (
  `path_name` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://dq-test-lambda-functions-unittest/exclude/default'
TBLPROPERTIES (
  'classification'='parquet',
  'parquet.compression'='SNAPPY',
  'transient_lastDdlTime'='1589292263')

  SELECT * FROM "bitd_input_test"."input_file_bitd_output_unittest" limit 10;



SHOW PARTITIONS input_file_bitd_output_unittest;

ALTER TABLE bitd_input_test.input_file_bitd_output_unittest
ADD PARTITION(path_name="outputfile/")
LOCATION 's3://dq-test-lambda-functions-unittest/outputfile/';

'''
