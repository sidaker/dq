import boto3
from collections import defaultdict
import threading
import os
import botocore
import json
import logging
from urllib.parse import unquote
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)

"""
Setup Logging
"""


LOG_FILE = "/Users/sbx/Documents/tmp//xxxx_hist.log"


PROFILE="notprod"
BUCKET_N='s3-dq-xxxx-archive-notprod'
PREFIX_F='2018'

LOGFORMAT = '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'
FORM = logging.Formatter(LOGFORMAT)
logging.basicConfig(
    format=LOGFORMAT,
    level=logging.INFO
)
if logger.hasHandlers():
    logger.handlers.clear()
LOGHANDLER = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=7)
LOGHANDLER.suffix = "%Y-%m-%d"
LOGHANDLER.setFormatter(FORM)
CONSOLEHANDLER = logging.StreamHandler()
CONSOLEHANDLER.setFormatter(FORM)
logger.addHandler(CONSOLEHANDLER)
logger.info("Starting")

def get_matching_s3_objects(bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    print(f"-------INSIDE GET matching objects---------ok delete {bucket} {prefix} {suffix}  {PROFILE}")
    session = boto3.Session(profile_name=PROFILE)
    s3 = session.client('s3')
    paginator = s3.get_paginator("list_objects_v2")

    kwargs = {'Bucket': bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix, )
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = key_prefix

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                return

            for obj in contents:
                key = obj["Key"]
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    print(f"-------INSIDE GET matching keys---------ok delete {bucket} {prefix} {suffix}")
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj["Key"]


def download(myfile):
    session = boto3.Session(profile_name=PROFILE)
    s3 = session.resource('s3')
    try:
        file_name = unquote(myfile.split('/')[-1])
        download_path = '/Users/sbx/Documents/tmp/{}'.format(file_name)
        s3.Bucket(BUCKET_N).download_file(myfile, download_path)
    except botocore.exceptions.ClientError as e:
       if e.response['Error']['Code'] == "404":
           print("The object does not exist." , e)
       else:
           raise
    return 200


def upload(myfile):
    session = boto3.Session(profile_name=PROFILE)
    s3 = session.resource('s3')
    try:
        s3.Bucket(BUCKET_N).upload_file(myfile, f'/Users/sbx/Documents/{myfile}')
    except botocore.exceptions.ClientError as e:
       if e.response['Error']['Code'] == "404":
           print("The object does not exist." , e)
       else:
           raise
    return 200


def build_new_fpl_json(input_json):
    """Given an input FPL dict
    Strip out the non x400message key and add all its subkeys
    as top level keys of a new dict

    Args:
    input_json - dict

    Returns:
    Dict
    """
    new_json = {}
    for key in input_json.keys():
        if key.lower() == 'x400message':
            new_json[key] = json.dumps(input_json[key])
        else:
            for sub_key in input_json[key]:
                new_json[sub_key] = input_json[key][sub_key]
            new_json['MessageType'] = key
    new_json['messageReceievedTime'] = input_json['X400Message']['envelope']['messageDeliveryTime']
    return new_json

def extract_message_received_time(input_json):
    """Extract the departure date from the xxxx field
    and return as datestring in the form 'YYYY-MM-DD'
    """
    date_str = input_json['messageReceievedTime']
    return f'msg_date=20{date_str[0:2]}-{date_str[2:4]}-{date_str[4:6]}'

def upload_file_s3(file_location, partition_str):
    """Uploads file to s3"""
    try:
        logger.info('Uploading {0}'.format(file_location))
        output_bucket = "s3-dq-xxxx-internal-notprod/processed/fpl"
        session = boto3.Session(profile_name=PROFILE)
        s3_conn = session.resource('s3')
        file_name = file_location.split('/')[-1]
        bucket = output_bucket.split('/')[0]
        output_path = '/'.join(output_bucket.split('/')[1:]) + '/' + partition_str
        print("-----", output_path)
        if os.path.getsize(file_location) != 0:
            s3_conn.Bucket(bucket).upload_file(file_location, '{0}/{1}'.format(output_path, file_name))
            logger.info('Upload complete')
        else:
            logger.info('Empty file, skipping upload')
    except Exception as e:
        logger.info('Failed to upload')
        logger.info(e)
        raise

def process_fpl(file_name):
    BASE_PATH = '/Users/sbx/Documents/tmp/'
    with open(f'{BASE_PATH}/{file_name}', 'r') as f:
        data = f.read()

    json_data = json.loads(data)
    new_json = build_new_fpl_json(json_data)
    new_json['filename'] = file_name
    new_json['entirejson'] = json_data
    partition_str = extract_message_received_time(new_json)

    with open(f'/{BASE_PATH}/parsed_{file_name}', 'w') as new_f:
        new_f.write(json.dumps(new_json))

    upload_file_s3(f'/Users/sbx/Documents/tmp/parsed_{file_name}', partition_str)
    return {'partition': partition_str, 'file_name': f'parsed_{file_name}'}


logger.info('Geting List of S3 Files for Download')
new_dict = defaultdict(list)
i=0
for n,key in enumerate(get_matching_s3_keys(bucket=BUCKET_N, prefix=PREFIX_F, suffix='.json')):
    if(n % 30 == 0):
        i=i+1
    new_dict['batch' + str(i)].append(key)
    if(i == 5):
        break

print(new_dict)
print (f"So, from bucket: {BUCKET_N} , download files with prefix: {PREFIX_F}")
logger.info('Starting fpl parsing process')
j=1
for j in range(1,6):
    for fname in new_dict['batch' + str(j)] :
        print("Processing file:", fname, " Batch", str(j))
        threading.Thread(target = download, args=(fname,)).start()
    j=j+1

#loop
#processed_fpl = process_fpl(file_name)

j=1
for j in range(1,6):
    for fname in new_dict['batch' + str(j)] :
        print("Processing file:", fname, " Batch", str(j))
        file_name_up = unquote(fname.split('/')[-1])
        processed_fpl = process_fpl(file_name_up)
    j=j+1


logger.info('Done')
