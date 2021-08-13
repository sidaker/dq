import json
import jsonschema
from jsonschema import validate


def get_schema():
    """This function loads the given schema available"""
    with open('/Users/sbommireddy/Downloads/COR-2004/JSON_SNSGB.json', 'r') as file:
        schema = json.load(file)
    return schema


execute_api_schema = get_schema()
print(execute_api_schema)
