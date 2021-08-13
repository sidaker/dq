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


def execute_glue_api(database_name, tb_name, partition_val):
    """
    Function that calls glue's batch create partition API.
    """
    try:
        gluesession = boto3.Session(profile_name='prod')
        glue_client = gluesession.client("glue", "eu-west-2")
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
    #partitions = party["Values"]
    #print(party)
    #print(partitions)

    #print(len(partitions))
    batch = 100
    #print(len(party))

    for idx,vals in enumerate(party["Values"]):

        #to_delete = [{k:v[k]} for k,v in zip(["Values"]*batch, partitions[idx:idx+batch])]
        #print(to_delete)
        #for i in range(25):
        print(vals)
        partition_list = [{'Values': [vals]}]
        print(partition_list)
        execute_glue_api(db_name, tb_name, partition_list)
        #partition_list =[{'Values': ['2020-08-13/06:24:10.770950']}, {'Values': ['2020-08-13/08:02:33.595458']}]
