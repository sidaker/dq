
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
            listb = [{'Values': d['Values']} for d in resp['Partitions'] ]

            x = [[]]
            for idx,val in enumerate(listb):
                 x[0].append(val)

            #print(len(x))
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

    boto3.setup_default_session(profile_name='prod')
    database_name='internal_reporting_prod'
    table_name='dim_parsed_message'
    retention = str(THIRTYDAYS)

    CONFIG = Config(
        retries=dict(
            max_attempts=10
        )
    )

    GLUE = boto3.client('glue', config=CONFIG , region_name='eu-west-2')

    # Below code converts the entire generator to a list.
    # lst = list(get_partitions(database_name, table_name))
    # print(len(lst))
    # print(lst)

    ct = 0
    it = iter(get_partitions(database_name, table_name))
    while True:
        #pass
        try:
            # be careful not to call a new iterator everytime
            parts = list(next(it))
            print(len(parts))
            print(parts)
            ct += 1
            if(ct>3):
                break

        except StopIteration:
            break

    # yields one partition at a time
    for parts in get_partitions(database_name, table_name):
        #print(parts)
        #print(len(parts))
        #newparts = list(filter(lambda d: d['Values'] in keyValList, parts))
        #newparts = list(filter(lambda d: False if d['Values'] in '2020-08-04/180019' else True , parts))
        #print(newparts)
        break
        # lambda x: True if x % 2 == 0 else False
        #match = PATTERN.search(vals).group(0)
        #PATTERN.search
        # selected_files = list(filter(regex.search, files))
        # Use filter to implement retention
