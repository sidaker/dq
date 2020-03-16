import os
import json
import logging
import os
import sys
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def build_new_fpl_json(input_json):
    """Given an input  dict
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

    return new_json


def process_fpl(file_name):
    BASE_PATH = '/Users/sbommireddy/Documents/python/assignments/dq/src/'
    with open(f'{BASE_PATH}/{file_name}', 'r') as f:
        data = f.read()

    # read json data using json.loads and convert json into a dictionary.
    json_data = json.loads(data)
    # parse dictionary
    new_json = build_new_fpl_json(json_data)


    with open(f'/{BASE_PATH}/parsed_{file_name}', 'w') as new_f:
        new_f.write(json.dumps(new_json))

    '''
    Reads JSON file. Initial JSON has two elements.
    The non X400Message is further split resulting into more JSON elements.
    message receive time is used to derive partition name.
    Parsed JSON file is  written
    '''



file_path = '/tmp/input_j.json'
processed_fpl = process_fpl(file_path)
