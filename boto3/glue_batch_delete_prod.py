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
    #results = glue_client.get_partitions(DatabaseName=database,TableName=table)
    # Bug only 124 retrieved.
    # Use next token
    #print(results)

    kwargs = {
        'DatabaseName' : database,
        'TableName' : table,
        'Expression' : "path_name like '2020-07-1%'",
        'MaxResults' : 999,

    }

    while True:
        resp = glue_client.get_partitions(**kwargs)
        yield from resp['Partitions']
        try:
            kwargs['NextToken'] = resp['NextToken']
        except KeyError:
            break

    #partitions = results["Partitions"]
    #print(len(partitions))
    '''
    for i in range(0, len(partitions), batch):
        to_delete = [{k:v[k]} for k,v in zip(["Values"]*batch, partitions[i:i+batch])]
        print(to_delete)
        partition_list = to_delete
    '''

def execute_glue_api(database_name, tb_name, partition_val):
    """
    Function that calls glue's batch delete partition API.
    """
    try:
        gluesession = boto3.Session(profile_name='prod')
        glue_client = gluesession.client("glue", "eu-west-2")
        glue_client.batch_delete_partition(DatabaseName=database_name, TableName=tb_name, PartitionsToDelete=partition_val)
        print("Dropped:", partition_val)
    except ClientError as err:
        if err.response['Error']['Code'] in 'EntityNotFoundException':
            err = 'Table ' + database_name + '.' + tb_name + ' partitions'  + ' not found!'
            LOGGER.warning(err)
        else:
            print(err)

db_name='api_input_prod'
tb_name='input_file_api'
#partition_list = [{'Values': ['path_name=2020-07-11%2F15%3A34%3A12.000000']}, {'Values': ['path_name=2020-07-11%2F22%3A41%3A30.000000']}]

#generator = get_partitions(db_name, tb_name)


for party in get_partitions(db_name, tb_name):
    #print(party)
    #print(len(party))
    partitions = party
    #partitions = party["Values"]
    #print(party)
    #print(partitions)

    #print(len(partitions))
    batch = 25
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
        


#execute_glue_api(db_name, tb_name, partition_list)
#print(partition_list)
