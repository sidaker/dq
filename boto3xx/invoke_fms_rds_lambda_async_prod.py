import logging
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import os
from os import path
import shutil
import json
import boto3
import time
import csv

def path_exists(path2):
    return path.exists(path2)

def dir_exists(path2):
    return path.isdir(path2)

def invoke_lambdaf(env, lambdaf, payx):
    session = boto3.Session(profile_name=env)
    lambda_client = session.client("lambda", "eu-west-2")

    # 'FunctionName' : 'arn:aws:lambda:eu-west-2:483846886818:function:api-cross-record-scored-notprod-lambda-athena',
    # 'InvocationType' : 'DryRun',
    # 'InvocationType' : 'DryRun',
    kwargs = {
        'FunctionName' : lambdaf ,
        'Payload' : json.dumps(payx),
        'InvocationType' : 'Event',
        'LogType' : 'None',

    }


    resp = lambda_client.invoke(**kwargs)
    logging.info(f'Response: {resp}')
    return resp



if __name__ == '__main__':
    st_dttime =  datetime.now()
    env = 'prod'
    acc = '337779336338'
    # arn:aws:lambda:eu-west-2:337779336338:function:fms-prod-lambda-rds
    farn = f'arn:aws:lambda:eu-west-2:{acc}:function:fms-{env}-lambda-rds'
    print(farn)

    dire = '/Users/sbommireddy/Downloads/cloudwatchlogs/'  ## Modify this.
    filepath = '/Users/sbommireddy/Downloads/file2.txt' # Modify this.
    datetime.now().strftime("%Y-%m-%d%H%M%S")
    logfile = "lambda_" + datetime.now().strftime("%Y-%m-%d%H%M%S") +  ".log"

    print(path_exists(os.path.join(dire, env)))
    locallogfile= os.path.join(dire, env, logfile)

    fmtstr = "%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d %(message)s"
    datestr = '%m/%d/%Y %I:%M:%S %p'
    logging.basicConfig(level=logging.INFO,
                        filename=locallogfile,
                        filemode='w',
                        format=fmtstr,
                        datefmt=datestr)

    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    logging.info(f'Function ARN: {farn}')



    payx = {"Records": [{"expectedBucketName": "s3-dq-api-internal", "transformDir": "transform_tbl_api", "targetSchema": "dq_fms", "targetTable": "stg_tbl_api", "fileType": "csv", "rdsLoadEnabled": "True", "rdsPreLoadTransformDir": "None", "rdsPostLoadTransformDir": "None", "s3": {"s3SchemaVersion": "1.0", "configurationId": "tf-s3-lambda-20190423000831206600000001", "bucket": {"name": "s3-dq-api-internal-prod", "ownerIdentity": {"principalId": "A2LMAGV8QC99Y1"}, "arn": "arn:aws:s3:::s3-dq-api-internal-prod"}, "object": {"key": "log-fms/2020-10-01/15%3A40%3A16.957140207/trigger.csv", "size": 24, "eTag": "0d026e8ab90e9143e263b2eae5230f7f", "versionId": "zPeLYG_dCdeyiDJy8xkpL1M0nWmuB8JC", "sequencer": "005F77A92BD3695033"}}, "eventTime": "2020-10-07T13:38:00.408Z"}]}
    #read a file with .

    with open(filepath) as fp:
        for line in fp:
            # Generate Payload by updating the dict
            #payx['Records'][0]['s3']['object']['key'] = "log-fms/2020-10-01/15%3A40%3A16.957140208/trigger.csv"
            payx['Records'][0]['s3']['object']['key'] = line

            logging.info(f'Payload: {payx}')
            print(payx['Records'][0]['s3']['object']['key'])
            print(json.dumps(payx))

            #invoke lambda syncronously.

            lambda_resp = invoke_lambdaf(env, farn, payx)
            print(lambda_resp)
            scode =  lambda_resp['StatusCode']
            print(scode)


            time.sleep(160)






    print(datetime.now())
