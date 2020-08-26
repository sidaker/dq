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


def get_partitions(database, table):
    gluesession = boto3.Session(profile_name='prod')
    glue_client = gluesession.client("glue", "eu-west-2")

    kwargs = {
        'DatabaseName' : database,
        'TableName' : table,

    }

    while True:
        resp = glue_client.get_partitions(**kwargs)
        yield from resp['Partitions']
        try:
            kwargs['NextToken'] = resp['NextToken']
        except KeyError:
            break


db_name='api_input_prod'
tb_name='input_file_api'

'''
    for i in range(0, len(partitions), batch):
        part_list = [{k:v[k]} for k,v in zip(["Values"]*batch, partitions[i:i+batch])]
        print(part_list)
        partition_list = part_list
'''
i=0
for part in get_partitions(db_name, tb_name):
    print(part["Values"])
    print(part)
    i = i + 1

print(i)
