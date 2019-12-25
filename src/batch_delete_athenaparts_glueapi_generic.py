import boto3
from datetime import datetime
from botocore.exceptions import ClientError


session = boto3.Session(profile_name='notprod')
client = session.client('glue',region_name='eu-west-2')

startTime = datetime.now()

def execute_glue_api(DATABASE_NAME,TB_NAME,partition_val):
    try:
        client.batch_delete_partition(DatabaseName=DATABASE_NAME,TableName=TB_NAME,
        PartitionsToDelete=partition_val
        )
        print("Deleted Partitions. No errors seen")
    except ClientError as e:
        print('partition not exist',e.response['Error']['Code'])


DATABASE_NAME='api_input_notprod'
TB_NAME='input_file_api'
'''
partition_val=[
        {'Values': ['2019-12-03/12:22:33.567633']},
        {'Values': ['2019-12-03/12:24:33.975791']},
    ]
'''
''' Loop this Again and again '''

keydict = 'Values'
part_list = []
for part in   ['2019-12-03/12:25:34.203552','2019-12-03/12:26:34.440026'] :
    part_list.append({keydict:[part]})
print(part_list)
execute_glue_api(DATABASE_NAME,TB_NAME,part_list)


print(datetime.now() - startTime)
