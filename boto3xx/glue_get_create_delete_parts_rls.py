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



def create_partition(partlist, database_name, table_name):
    """
    Function that calls glue's batch create partition API.
    Pass atleast Values and Location
    HIVE_METASTORE_ERROR: com.facebook.presto.spi.PrestoException:
    Required Table Storage Descriptor is not populated.
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
    Remove Storae Descriptor Object if exists in input.
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


def get_partitions(database, table, retention):
    """
    Loop until the query is either successful or fails
    Args:
        database, table      : the submitted query execution id
    Returns:
        A list of partitions
    """
    # 'Expression' : "path_name < '2020-09-13'",

    myexp = f"path_name < '{retention}' "
    #myexp = "std_date_local < '2020-10-31' and std_date_local <> '1900-01-01'"
    #print(myexp)
    try:
        kwargs = {
            'DatabaseName' : database,
            'TableName' : table,
            'MaxResults' : 25,
            'Expression' : myexp  ,
            }

        while True:
            resp = GLUE.get_partitions(**kwargs)

            listb = [{'Values': d['Values'], 'StorageDescriptor': d['StorageDescriptor']} for d in resp['Partitions'] ]

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
    EIGHTYDAYS = (datetime.date.today() - datetime.timedelta(days=81))
    FOURDAYS = (datetime.date.today() - datetime.timedelta(days=12))
    TODAY = datetime.date.today()

    boto3.setup_default_session(profile_name='prod')
    database_name='api_record_level_score_prod'
    table_name='internal_storage_table'
    retention = str(EIGHTYDAYS)

    CONFIG = Config(
        retries=dict(
            max_attempts=10
        )
    )

    GLUE = boto3.client('glue', config=CONFIG , region_name='eu-west-2')

    # yields 25 partition at a time
    for parts in get_partitions(database_name, table_name, retention):
        #print(parts)
        #print(len(parts)) # max 25

        #create_partition(parts, database_name, f'{table_name}_archive')
        for d in parts:
            del d['StorageDescriptor']

        if(len(parts)>0):
            print(parts)
            #print(len(parts))
            #execute_glue_api_delete(database_name, table_name, parts)
