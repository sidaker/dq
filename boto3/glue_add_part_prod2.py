# batch_create_partition
# create_partition

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
        print(i)
        reate_partition_response = glue.batch_create_partition(
                DatabaseName=database_name,
                TableName=table_name,
                PartitionInputList=data
            )


def generate_partition_input(year, month, day, s3_input,table_data):

    part_location = "{}/{}-{}-{}/".format(s3_input, year, month, day)
    input_dict = {
        'Values': [
            year, month, day
        ],
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
        #month = str(date.month)
        #day = str(date.day)
        month = '{:02d}'.format(date.month)
        day =  '{:02d}'.format(date.day)

        #print(year)
        #print(month)
        #print(day)

        input_list.append(generate_partition_input(year, month, day, s3_input,table_data))

    return input_list

'''
def execute_glue_api(database_name, tb_name, partition_val):
    """
    Function that calls glue's batch create partition API.
    """
    try:

        glue_client.batch_create_partition(DatabaseName=database_name, TableName=tb_name, PartitionInputList=partition_val)
        print("Added:", partition_val)
    except ClientError as err:
        if err.response['Error']['Code'] in 'EntityNotFoundException':
            err = 'Table ' + database_name + '.' + tb_name + ' partitions'  + ' not found!'
            LOGGER.warning(err)
        else:
            print(err)

db_name='internal_reporting_prod'
tb_name='dim_person_on_a_voyage_archive'
#partition_list = [{'Values': ['path_name=2020-07-11%2F15%3A34%3A12.000000']}, {'Values': ['path_name=2020-07-11%2F22%3A41%3A30.000000']}]
# s3://s3-dq-reporting-internal-working-prod/dim_person_on_a_voyage/storage/2019-06-27/

for party in get_partitions(db_name, tb_name):

    partitions = party
    batch = 100

    for idx,vals in enumerate(party["Values"]):
        print(vals)
        partition_list = [{'Values': [vals]}]
        print(partition_list)
        execute_glue_api(db_name, tb_name, partition_list)
        #partition_list =[{'Values': ['2020-08-13/06:24:10.770950']}, {'Values': ['2020-08-13/08:02:33.595458']}]
'''

# Python program to use
# main for function call.
if __name__ == "__main__":
    gluesession = boto3.Session(profile_name='default')
    glue = gluesession.client("glue", "eu-west-2")

    #db_name='internal_reporting_prod'
    #tb_name='dim_person_on_a_voyage_archive'

    # Glue table location
    database_name = 'api_accuracy_score_test'  # update
    table_name = 'accuracy_scoring' # update

    # S3 info location
    s3_bucket_glue = 's3-dq-accuracy-score-test'    # update
    s3_prefix_glue = '' # update
    #s3_input_glue = 's3://' + s3_bucket_glue + '/' + s3_prefix_glue
    s3_input_glue = 's3://' + s3_bucket_glue

    # Desired time range
    start_time = datetime.now() + timedelta(days=-5)
    end_time = datetime.now() + timedelta(days=-2)

     # Get Glue table metadata
    table_data = get_current_schema(table_name, database_name)
    print(table_data)

    # Generate partition list of dicts
    data = generate_partition_input_list(start_time, end_time, s3_input_glue, table_data)
    print(data)
