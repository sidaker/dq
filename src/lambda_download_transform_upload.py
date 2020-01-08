import os
import json
import boto3
import logging
import os
from urllib.parse import unquote
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def extract_message_received_time(input_json):
    """Extract the departure date from the EOBD field
    and return as datestring in the form 'YYYY-MM-DD'
    """
    date_str = input_json['messageReceievedTime']
    return f'msg_date=20{date_str[0:2]}-{date_str[2:4]}-{date_str[4:6]}'

def process_fpl(file_name):
    BASE_PATH = '/tmp'
    with open(f'{BASE_PATH}/{file_name}', 'r') as f:
        data = f.read()

    json_data = json.loads(data)
    json_data['filename'] = file_name
    partition_str = extract_message_received_time(json_data)

    with open(f'/{BASE_PATH}/parsed_{file_name}', 'w') as new_f:
        new_f.write(json.dumps(new_json))

    upload_file_s3(f'/tmp/parsed_{file_name}', partition_str)
    return {'partition': partition_str, 'file_name': f'parsed_{file_name}'}

def upload_file_s3(file_location, partition_str):
    """Uploads file to s3"""
    try:
        logger.info('Uploading {0}'.format(file_location))
        # output_bucket_name is obtained from enviornment e.g. value s3-xx-xxx-internal-xxx/processed/xxx
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



def lambda_handler(event, context):
    logger.info('Starting processing of S3')
    s3_client = boto3.client('s3')
    total_records = len(event['Records'])
    counter = 1
    for record in event['Records']:
        logger.info('Processing record {0} of {1}'.format(counter, total_records))
        logger.info('Record name: {0}'.format(record['s3']['object']['key']))
        bucket = record['s3']['bucket']['name']
        key = unquote(record['s3']['object']['key'])
        file_name = unquote(key.split('/')[-1])
        download_path = '/tmp/{}'.format(file_name)
        s3_client.download_file(bucket, key, download_path)
        processed_fpl = process_fpl(file_name)
        logger.info('Done')
    logger.info('Done')
    return { 'statusCode': 200 }
