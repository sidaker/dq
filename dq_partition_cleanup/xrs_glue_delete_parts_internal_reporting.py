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
import pandas as pd
import ast




def execute_glue_api_delete(database_name, tb_name, partition_val):
    """
    Function that calls glue's batch delete partition API.
    Remove Storae Descriptor Object if exists in input.
    """
    try:

        GLUE.batch_delete_partition(DatabaseName=database_name, TableName=tb_name,
        PartitionsToDelete=[{'Values': partition_val}]
        )
        print("Dropped:", partition_val)
    except ClientError as err:
        if err.response['Error']['Code'] in 'EntityNotFoundException':
            err = 'Table ' + database_name + '.' + tb_name + ' partitions'  + ' not found!'
            LOGGER.warning(err)
            print(err)
        else:
            LOGGER.error(err)


if __name__=='__main__':
    # Change the profile of the default session in code
    PATTERN = re.compile("20[0-9]{2}-[0-9]{1,2}-[0-9]{1,2}")
    TWOMONTHSPLUSCURRENT = ((datetime.date.today() - relativedelta(months=2)).replace(day=1) - datetime.timedelta(days=1))
    THIRTYDAYS = (datetime.date.today() - datetime.timedelta(days=30))
    EIGHTYDAYS = (datetime.date.today() - datetime.timedelta(days=150))
    FOURDAYS = (datetime.date.today() - datetime.timedelta(days=12))
    TODAY = datetime.date.today()

    boto3.setup_default_session(profile_name='prod')
    database_name='internal_reporting_prod'
    table_name='dim_carrier'
    retention = str(EIGHTYDAYS)

    CONFIG = Config(
        retries=dict(
            max_attempts=2
        )
    )

    GLUE = boto3.client('glue', config=CONFIG , region_name='eu-west-2')

    # yields 25 partition at a time
    mycsvfile = '/Users/sbommireddy/Downloads/cloudwatchlogs/prod/consolidated_partitions_2022-05-11-02145937.csv'

    # Create a dataframe from csv
    df = pd.read_csv(mycsvfile, delimiter=',')
    # User list comprehension to create a list of lists from Dataframe rows
    list_of_rows = [list(row) for row in df.values]
    # Print list of lists i.e. rows
    print(list_of_rows)

    for eachlist in list_of_rows:
        arg_std = eachlist[0]
        arg_ppt = eachlist[1]
        std_date = arg_std[2:12]
        arg_std = ast.literal_eval(arg_std)

        execute_glue_api_delete(database_name, table_name, arg_std )
