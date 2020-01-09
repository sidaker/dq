import os
import json
import logging
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
    BASE_PATH = "/Users/siddharthabommireddy/Desktop/Python/sidgitrepo/dq/src"
    with open(f'{file_name}', 'r') as f:
        data = f.read()

    json_data = json.loads(data)
    print(type(json_data))
    print(type(data))
    json_data['filename'] = file_name
    partition_str = extract_message_received_time(json_data)

    with open(f'/{BASE_PATH}/new_file.json', 'w') as new_f:
        new_f.write(json.dumps(json_data))

    return {'partition': partition_str}

def main():
    logger.info('Starting processing of S3')
    #Modify this
    processed_fpl = process_fpl("/Users/siddharthabommireddy/Desktop/Python/sidgitrepo/dq/src/likhibargu.json")
    print(processed_fpl)
    logger.info('Done')

if __name__ == '__main__':
    main()
