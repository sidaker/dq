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


# arn = arn:aws:lambda:eu-west-2:337779336338:function:api-cross-record-scored-prod-lambda-athena
# arn = arn:aws:lambda:eu-west-2:483846886818:function:api-cross-record-scored-notprod-lambda-athena
#env = 'prod'
#acc = '337779336338'

if __name__ == '__main__':
    st_dttime =  datetime.now()
    env = 'prod'
    acc = '337779336338'
    farn = f'arn:aws:lambda:eu-west-2:{acc}:function:api-cross-record-scored-{env}-lambda-athena'

    dire = '/Users/sbommireddy/Downloads/cloudwatchlogs/'
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
    #session = boto3.Session(profile_name=env)
    #lclient = session.client('lambda', region_name='eu-west-2')
    logging.info(f'Function ARN: {farn}')

    cdate= "2019-10-12"
    #high_water_mark=''
    with open(os.path.join('/tmp','highwatermark.csv')) as f:
        reader = csv.reader(f)
        high_water_mark = next(reader)  # gets the first line
        cdate = high_water_mark[0]
        logging.info('High Water Mark: %s', high_water_mark)
        print(high_water_mark)
        print(f'Read Process date to {cdate}')

    payx = { "minStdDateLocal": cdate,"maxStdDateLocal": cdate, "Records": [{ "partitionConsolidateTarget": "True", "tableName": "internal_storage_by_std_date_local"}]}

    while(True):
        cdate = (datetime.strptime(cdate, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        # Generate Payload by updating the dict
        payx['minStdDateLocal'] = cdate
        payx['maxStdDateLocal'] = cdate
        logging.info(f'Consolidating Partitions for {cdate}')
        logging.info(f'Payload: {payx}')
        #logging.info(f'Consolidating Partitions for {cdate}')
        #logging.info(f'Payload: {payx}')
        print(cdate)
        print(json.dumps(payx))

        #invoke lambda syncronously.
        lambda_resp = invoke_lambdaf(env, farn, payx)
        print(lambda_resp)
        scode =  lambda_resp['StatusCode']
        #print(scode)
        # Break and dont invoke further if program is running for more than x or 90 minutes.
        curr_dttime = datetime.now()
        print(curr_dttime)
        print(curr_dttime - st_dttime)
        difference = curr_dttime - st_dttime
        seconds_in_day = 24 * 60 * 60
        # timedelta(0, 8, 562000)
        a =divmod(difference.days * seconds_in_day + difference.seconds, 60)
        print(a[0])
        #print(a[1])
        logging.info(f'time elapsed: {a}')

        # 8 18 minutes
        # 16  26 minutes
        # 50  60 minutes
        # 75  84 minutes
        if a[0] > 19 :
            print("Exiting....")
            print(a[0])
            logging.error(f'Exiting.: {a}')
            with open("/tmp/highwatermark.csv", "w") as f:
                f.write(cdate)
                print(f'Updated Process date to {cdate}')
            break


        print("-"*50)
        # Wait for 490 seconds
        time.sleep(360)

    print(datetime.now())
