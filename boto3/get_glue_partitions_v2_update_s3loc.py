import sys
import time
import random
import os
import urllib.request
import json
import logging
import pprint
from logging.handlers import TimedRotatingFileHandler
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import datetime
import csv
from urllib.parse import unquote
from urllib.parse import urlparse
from datetime import datetime

env='prod'

'''
def glue_update_part(glue_database,tbl_name):
    glue = boto3.client('glue', region_name='eu-west-2')
    glue.update_partition(
        DatabaseName=glue_database,
        TableName=tbl_name,
        PartitionValueList=key['Values'],
        PartitionInput=key
            )
'''

def prefix_exists(bucket_name, prefix):
    """
    AWS guarantee that an S3 event notification will be delivered at least once.
    If the prefix exists in the target bucket / location, the event is ignored
    """
    try:
        result = False
        s3session = boto3.Session(profile_name='prod')
        s3_client = s3session.client("s3", "eu-west-2")
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )
        if response.get('Contents'):
            result = True
        else:
            pass

        return result

    except Exception as err:
        print('Error Occured while checking for S3 key')

def get_partitions(database, table):
    gluesession = boto3.Session(profile_name='prod')
    glue_client = gluesession.client("glue", "eu-west-2")

    kwargs = {
        'DatabaseName' : database,
        'TableName' : table,
        'Expression' : "std_date_local < '2020-03-20'",
        'MaxResults' : 999,

    }

    while True:
        resp = glue_client.get_partitions(**kwargs)
        yield from resp['Partitions']
        try:
            kwargs['NextToken'] = resp['NextToken']
        except KeyError:
            break


db_name='api_cross_record_scored_prod'
tb_name='internal_storage_by_std_date_local_recent'
#bucket_name = 's3-dq-cross-record-scored-prod'


i=0
j=0
local_output_dir='/Users/sbommireddy/Downloads/cloudwatchlogs/'
ts = datetime.today().strftime('%Y-%m-%d-%H%M%S')
# str(datetime.now())
filename = 'partitions_'  + ts + '.csv'
logfile = os.path.join(local_output_dir, env, filename)
print(logfile)

with open(logfile, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PartitionName", "DB_Name","Table_name","Location","S3key","newS3", "NewLocation"])


    for part in get_partitions(db_name, tb_name):
        mys3session = boto3.Session(profile_name='prod')
        client = mys3session.client("s3", "eu-west-2")
        glue = mys3session.client('glue', 'eu-west-2')
        locate = part["StorageDescriptor"]["Location"]
        partsvals = part["Values"]
        partsdb = part["DatabaseName"]
        partstb = part["TableName"]
        newlo = ''
        #s3key = 'internal_storage_by_std_date_local/20191123115056/std_date_local=2019-11-23/'
        file_name = unquote(locate.split('/')[-1])
        oparse = urlparse(locate, allow_fragments=False)
        bucket_name = oparse.netloc
        s3key = oparse.path

        s3key = s3key.lstrip('/')
        s3keyex = prefix_exists(bucket_name, s3key)
        mods3key = s3key.replace(':','%3A') # Replace : with %3A
        if(s3keyex):
            news3keyex=False
        else:
            news3keyex =  prefix_exists(bucket_name, mods3key)

        if(news3keyex):
            #print("Update this Partition Location with %s",mods3key)
            j= j+1
            oldlo = part['StorageDescriptor']['Location']
            print("old location:",oldlo)
            part['StorageDescriptor']['Location'] = 's3://' + part['StorageDescriptor']['Location'][5:].replace(':', '%3A')
            del part['TableName']
            del part['DatabaseName']
            del part['CreationTime']
            #print("Updating with the following input")
            newlo = part['StorageDescriptor']['Location']
            print("new location:",newlo)
            #pprint.pprint(part)
            #print('New Location: ' + part['StorageDescriptor']['Location']);
            s3_path = part['StorageDescriptor']['Location'].split('/')
            bucket_name_part = s3_path[2]
            s3_prefix_part = "/".join(s3_path[3:]) + "/"
            #print("s3_prefix: " + s3_prefix_part)
            response = client.list_objects_v2(Bucket=bucket_name_part, Delimiter='/', MaxKeys=1, Prefix=s3_prefix_part)
            if 'Contents' in response:
                print("Updating Partition Location",part['Values'])
                glue.update_partition(
                    DatabaseName=partsdb,
                    TableName=partstb,
                    PartitionValueList=part['Values'],
                    PartitionInput=part
                            )
            else:
                print("Invalid S3 path")

        writer.writerow([partsvals, partsdb, partstb,locate, s3keyex, news3keyex , newlo ])
        i = i + 1

print("total partitions:",i)
print("Updated Partitions:",j)


# Where S3 Key is False for those partitions check if the location exists if : is replaced by %3A
# Check if each of the key exists.
# Update the Partition Location.
#print(prefix_exists('s3-dq-cross-record-scored-prod', 'internal_storage_by_std_date_local/20191123115056/std_date_local=2019-11-23/'))
