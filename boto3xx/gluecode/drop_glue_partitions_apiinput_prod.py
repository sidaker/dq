import sys
import time
import random
import csv
import re
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
    Function that calls glue's batch delete partition API.
    """
    try:
        client = boto3.client('glue', config=CONFIG)
        client.batch_delete_partition(DatabaseName=database_name, TableName=tb_name, PartitionsToDelete=partition_val)
    except ClientError as err:
        if err.response['Error']['Code'] in 'EntityNotFoundException':
            err = 'Table ' + database_name + '.' + tb_name + ' partitions'  + ' not found!'
            LOGGER.warning(err)
        else:
            print(err)

def lambda_handler(event, context):
    """
    Respond to an SNS notification.

    Args:
        event (dict)           : Data about the triggering event
        context (LamdaContext) : Runtime information

    Returns:
        null
    """
    #db_name = 'api_input_notprod'
    #tb_name = 'input_file_api'
    db_name='api_input_prod'
    tb_name='input_file_api'
    partition_list =['path_name=2020-08-13/06:24:10.770950','path_name=2020-08-13/08:02:33.595458']


    execute_glue_api(db_name, tb_name, partition_list)
