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



def get_and_delete_partitions(database, table, batch=25):
    gluesession = boto3.Session(profile_name='notprod')
    glue_client = gluesession.client("glue", "eu-west-2")
    partitions = glue_client.get_partitions(
        DatabaseName=database,
        TableName=table)["Partitions"]

    print(len(partitions))

    for i in range(0, len(partitions), batch):
        to_delete = [{k:v[k]} for k,v in zip(["Values"]*batch, partitions[i:i+batch])]
        print(to_delete)
        partition_list = to_delete


def execute_glue_api(database_name, tb_name, partition_val):
    """
    Function that calls glue's batch delete partition API.
    """
    try:
        gluesession = boto3.Session(profile_name='notprod')
        glue_client = gluesession.client("glue", "eu-west-2")
        #client = boto3.client('glue')
        glue_client.batch_delete_partition(DatabaseName=database_name, TableName=tb_name, PartitionsToDelete=partition_val)
        print("Dropped:", partition_val)
    except ClientError as err:
        if err.response['Error']['Code'] in 'EntityNotFoundException':
            err = 'Table ' + database_name + '.' + tb_name + ' partitions'  + ' not found!'
            LOGGER.warning(err)
        else:
            print(err)


db_name='api_record_level_score_notprod'
tb_name='internal_storage_table'
#partition_list =[{'Values': ['2020-08-13/06:24:10.770950']}, {'Values': ['2020-08-13/08:02:33.595458']}]
partition_list = [{'Values': ['path_name=2020-08-13/06:42:29.122926']}, {'Values': ['path_name=2020-08-13/07:09:32.231512']}]


get_and_delete_partitions(db_name, tb_name, 25)
execute_glue_api(db_name, tb_name, partition_list)
print(partition_list)
