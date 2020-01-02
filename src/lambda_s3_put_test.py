import json
import csv



def get_tables_to_drop(csv_fname):
    with open(csv_fname, "r") as drop_tables:
        for table in csv.reader(drop_tables):
            yield table

def lambda_handler(event, context):
    print("--------------")
    print(event['Records'][0]['s3']['object']['key'])
