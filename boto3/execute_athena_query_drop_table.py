import boto3
import csv
import os
import time

env='notprod'
dbname='api_record_level_score_notprod'
#dbname='api_input_notprod'
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
session = boto3.Session(profile_name=env)
aclient = session.client('athena', region_name='eu-west-2')

'''
Pre Req: Create csv
refer: glue/gte_list_tables_in_db_v2.py
'''

csvfilepath='/Users/sbommireddy/Downloads/cloudwatchlogs/notprod/drop_csv_working_cs.csv'
myqe={
        'Database': 'dbname',
        'Catalog': 'AwsDataCatalog'
    }

with open(csvfilepath) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for ct,row in enumerate(readCSV,1):
        #print(row[0])
        myquery = 'DROP TABLE IF EXISTS ' + dbname + '.' + row[0]
        print(myquery)

        response = aclient.start_query_execution(QueryString=myquery,
                                            QueryExecutionContext=myqe,
                                            ResultConfiguration={'OutputLocation': 's3://s3-dq-athena-log-notprod/'})

        query_execution_id = response['QueryExecutionId']
        print (query_execution_id)
        resp = aclient.get_query_execution(QueryExecutionId=query_execution_id)
        print(resp['QueryExecution']['Status']['State'])
        #time.sleep(2)
        #print(resp)
