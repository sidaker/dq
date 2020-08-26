import boto3
import csv
import os
import time
import botocore
from urllib.parse import unquote
from urllib.parse import urlparse

def download_froms3(myfile):
        #session = boto3.Session(profile_name=PROFILE)
        boto_s3_session = boto3.Session(profile_name=env)
        s3 = boto_s3_session.resource('s3')
        s3client = boto_s3_session.client('s3', region_name='eu-west-2')
        try:
            file_name = unquote(myfile.split('/')[-1])
            oparse = urlparse(myfile, allow_fragments=False)
            print(oparse)
            S3_SRC_BUCKET_NAME = oparse.netloc
            key = oparse.path
            download_path = '{0}{1}'.format(BASE_PATH,file_name)
            print(f'Downloading  from {S3_SRC_BUCKET_NAME} , {key} to {download_path} ')
            #s3.Bucket(S3_SRC_BUCKET_NAME).download_file(key, download_path)
            #s3.Bucket(S3_SRC_BUCKET_NAME).download_file(file_name, download_path)
            s3client.download_file(S3_SRC_BUCKET_NAME,file_name,download_path)
            print('File Downloaded')
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == "404":
                print("The object does not exist." , err)
            else:
                #raise
                error = str(err)
                print(error)

        return myfile

def check_query_status(execution_id):
    """
    Loop until the query is either successful or fails

    Args:
        execution_id             : the submitted query execution id

    Returns:
        None
    """
    try:
        #client = boto3.client('athena', config=CONFIG)
        session = boto3.Session(profile_name=env)
        client = session.client('athena', region_name='eu-west-2')

        while True:
            response = client.get_query_execution(
                QueryExecutionId=execution_id)
            if response['QueryExecution']['Status']['State'] in ('FAILED', 'SUCCEEDED', 'CANCELLED'):
                return response

            time.sleep(1)

    except Exception as err:
        print(err)


#env='notprod'
env='prod'
#dbname='api_record_level_score_notprod'
#dbname='api_input_notprod'
#dbname='api_record_level_score_notprod'
dbname='api_input_prod'
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
session = boto3.Session(profile_name=env)
aclient = session.client('athena', region_name='eu-west-2')
BASE_PATH = '/Users/sbommireddy/Downloads/'

myqe={
        'Database': dbname,

    }

#cond = "\'2020-08-21/%\'"
#myquery = 'select xml_file_name from api_record_level_score_notprod.internal_storage where path_name like  ' + cond
cond1 = "path_name like \'2020-08-21/08%\' or "
cond2 = "path_name like \'2020-08-21/09%\' or "
cond3 = "path_name like \'2020-08-21/10%\'"
myquery = 'select xml_file_name from api_input_prod.input_file_api where  ' + cond1 + cond2 + cond3
#athena_buck = 's3://s3-dq-athena-log-notprod/'
athena_buck = 's3://s3-dq-athena-log-prod/'
print(myquery)


response = aclient.start_query_execution(QueryString=myquery,
                                        QueryExecutionContext=myqe,
                                        ResultConfiguration={'OutputLocation': athena_buck})

query_execution_id = response['QueryExecutionId']
print (query_execution_id)
resp = aclient.get_query_execution(QueryExecutionId=query_execution_id)
#print(resp['QueryExecution']['Status']['State'])

### Keep looking till execution state is  Success or Failed.
#time.sleep(2)
#print(resp)

query_result = check_query_status(query_execution_id)
print(query_result)

'''
{'QueryExecution': {'QueryExecutionId': '1ff4945c-ce8e-4db3-89d6-2b8d4524862a', 'Query': "select xml_file_name from api_record_level_score_notprod.internal_storage where path_name like  '2020-08-21/%'", 'StatementType': 'DML', 'ResultConfiguration': {'OutputLocation': 's3://s3-dq-athena-log-notprod/1ff4945c-ce8e-4db3-89d6-2b8d4524862a.csv'}, 'QueryExecutionContext': {'Database': 'api_record_level_score_notprod'}, 'Status': {'State': 'SUCCEEDED', 'SubmissionDateTime': datetime.datetime(2020, 8, 21, 11, 8, 11, 344000, tzinfo=tzlocal()), 'CompletionDateTime': datetime.datetime(2020, 8, 21, 11, 8, 22, 966000, tzinfo=tzlocal())}, 'Statistics': {'EngineExecutionTimeInMillis': 11400, 'DataScannedInBytes': 114006838, 'TotalExecutionTimeInMillis': 11622, 'QueryQueueTimeInMillis': 221, 'QueryPlanningTimeInMillis': 4353, 'ServiceProcessingTimeInMillis': 1}, 'WorkGroup': 'primary'}, 'ResponseMetadata': {'RequestId': '00a64a4e-f32a-4446-b07f-73b171ca79a6', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Fri, 21 Aug 2020 10:08:22 GMT', 'x-amzn-requestid': '00a64a4e-f32a-4446-b07f-73b171ca79a6', 'content-length': '1512', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}

'''
print(query_result['QueryExecution']['ResultConfiguration'])
print(query_result['QueryExecution']['ResultConfiguration']['OutputLocation'])

file_location = query_result['QueryExecution']['ResultConfiguration']['OutputLocation']

## Download file.
download_froms3(file_location)
print("We are DONE")
