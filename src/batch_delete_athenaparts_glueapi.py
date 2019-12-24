import boto3
from datetime import datetime
from botocore.exceptions import ClientError


session = boto3.Session(profile_name='notprod')
client = session.client('glue',region_name='eu-west-2')

startTime = datetime.now()

def execute_glue_api(DATABASE_NAME,TB_NAME,partition_val):
    try:
        client.batch_delete_partition(DatabaseName=DATABASE_NAME,TableName=TB_NAME,
        PartitionsToDelete=[
                {'Values': ['2019-12-03/12:21:33.303976']},
                {'Values': ['2019-12-03/12:23:33.748611']},
            ]
        )
        print("Deleted Partitions. No errors seen")
    except ClientError as e:
        print('partition not exist',e.response['Error']['Code'])


DATABASE_NAME='api_input_notprod'
TB_NAME='input_file_api'
partition_val=['2019-12-03/12:23:33.748611']
execute_glue_api(DATABASE_NAME,TB_NAME,partition_val)


print(datetime.now() - startTime)
