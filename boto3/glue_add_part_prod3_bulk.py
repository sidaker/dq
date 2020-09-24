import sys
import time
import random
import os
import urllib.request
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from dateutil import rrule
from datetime import datetime, timedelta


def get_current_schema(table_name, database_name):

    response = glue.get_table(
        DatabaseName=database_name,
        Name=table_name)

    table_data = {}
    table_data['input_format'] = response['Table']['StorageDescriptor']['InputFormat']
    table_data['output_format'] = response['Table']['StorageDescriptor']['OutputFormat']
    table_data['table_location'] = response['Table']['StorageDescriptor']['Location']
    table_data['serde_info'] = response['Table']['StorageDescriptor']['SerdeInfo']
    table_data['partition_keys'] = response['Table']['PartitionKeys']

    return table_data


def create_partitions(data, database_name, table_name):

    break_list_in_chunks = lambda data, chunk: [data[x:x+chunk] for x in range(0, len(data), chunk)]

    for i, data in enumerate(break_list_in_chunks(data, 100)):
        print("-----------")
        print(i)
        print(data)
        create_partition_response = glue.batch_create_partition(
                DatabaseName=database_name,
                TableName=table_name,
                PartitionInputList=data
            )
        print(create_partition_response)


def generate_partition_input(year, month, day, s3_input,table_data):

    part_location = "{}/{}-{}-{}/".format(s3_input, year, month, day)
    value1 = "{}-{}-{}-history".format(year, month, day)
    input_dict = {
        'Values': [value1],
        'StorageDescriptor': {
            'Location': part_location,
            'InputFormat': table_data['input_format'],
            'OutputFormat': table_data['output_format'],
            'SerdeInfo': table_data['serde_info']
        }
    }

    return input_dict


def generate_partition_input_list(start, end, s3_input, table_data):

    input_list = []

    for date in rrule.rrule(rrule.DAILY, dtstart=start, until=end):

        year = str(date.year)
        month = '{:02d}'.format(date.month)
        day =  '{:02d}'.format(date.day)

        input_list.append(generate_partition_input(year, month, day, s3_input,table_data))

    return input_list


# Python program to use
# main for function call.
if __name__ == "__main__":
    gluesession = boto3.Session(profile_name='prod')
    glue = gluesession.client("glue", "eu-west-2")

    # Glue table location
    database_name = 'oag_transform_prod'  # update
    table_name = 'internal_storage_table_history' # update

    # S3 info location
    s3_bucket_glue = 's3-dq-oag-transform-prod'    # update
    s3_prefix_glue = 'bulk' # update
    s3_input_glue = 's3://' + s3_bucket_glue + '/' + s3_prefix_glue
    #s3_input_glue = 's3://' + s3_bucket_glue

    # Desired time range
    start_time = datetime.now() + timedelta(days=-656)
    end_time = datetime.now() + timedelta(days=-535)

     # Get Glue table metadata
    table_data = get_current_schema(table_name, database_name)
    print(table_data)

    # Generate partition list of dicts
    data = generate_partition_input_list(start_time, end_time, s3_input_glue, table_data)
    print("*"*50)
    print(data)

    #Batch insert partitions
    create_partitions(data, database_name, table_name)
