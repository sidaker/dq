import os
import json
import boto3
import logging
import os
import sys
from urllib.parse import unquote
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    # new code

    return new_json

def extract_message_received_time(input_json):
    """Extract the departure date from the EOBD field
    and return as datestring in the form 'YYYY-MM-DD'
    """
    date_str = input_json['messageReceievedTime']
    return f'msg_date=20{date_str[0:2]}-{date_str[2:4]}-{date_str[4:6]}'

def upload_file_s3(file_location, partition_str):
    """Uploads file to s3"""
    try:
        logger.info('Uploading {0}'.format(file_location))
        output_bucket = f"{os.environ.get('output_bucket_name')}"
        s3_conn = boto3.resource('s3')
        file_name = file_location.split('/')[-1]
        bucket = output_bucket.split('/')[0]
        output_path = '/'.join(output_bucket.split('/')[1:]) + '/' + partition_str
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
    BASE_PATH = '/Users/sbommireddy/Documents/python/assignments/dq/src/'
    with open(f'{BASE_PATH}/{file_name}', 'r') as f:
        data = f.read()

    json_data = json.loads(data)
    print(json_data)
    for dict in json_data.items():
        print(dict)
    print(len(json_data))
    #sys.exit()
    new_json = build_new_fpl_json(json_data)
    # new code
    new_json['filename'] = file_name
    new_json['entirejson'] = json_data

    print(new_json)

    print("-----------------")
    print(len(new_json))

    for dict in new_json.items():
        print(dict)

    with open(f'/{BASE_PATH}/parsed_{file_name}', 'w') as new_f:
        new_f.write(json.dumps(new_json))

    '''
    Reads JSON file. Initial JSON has two elements.
    The non X400Message is further split resulting into more JSON elements.
    message receive time is used to derive partition name.
    Parsed JSON file is  written
    '''

    sys.exit()
    upload_file_s3(f'/tmp/parsed_{file_name}', partition_str)
    return {'partition': partition_str, 'file_name': f'parsed_{file_name}'}

if __name__ == '__main__':
    file_name = 'input_j.json'
    processed_fpl = process_fpl(file_name)
