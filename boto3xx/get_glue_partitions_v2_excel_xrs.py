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
import datetime
import csv

env='prod'

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


db_name='api_cross_record_scored_prod'
tb_name='internal_storage_by_std_date_local'

'''
    for i in range(0, len(partitions), batch):
        part_list = [{k:v[k]} for k,v in zip(["Values"]*batch, partitions[i:i+batch])]
        print(part_list)
        partition_list = part_list
'''
i=0
local_output_dir='/Users/sbommireddy/Downloads/cloudwatchlogs/'
filename = 'partitions_'  + str(datetime.datetime.now()) + '.csv'
logfile = os.path.join(local_output_dir, env, filename)
print(logfile)

with open(logfile, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PartitionName", "DB_Name","Table_name","Location"])

    for part in get_partitions(db_name, tb_name):

        # print(part["Values"])
        # print(part["DatabaseName"])
        # print(part["TableName"])
        # print(part["StorageDescriptor"]["Location"])
        # cmd - /

        writer.writerow([part["Values"], part["DatabaseName"], part["TableName"],part["StorageDescriptor"]["Location"] ])
        #print(part)
        #exit()
        i = i + 1

print(i)
