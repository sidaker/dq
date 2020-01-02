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
MAX_RESULTS = 500
#response = client.get_partitions(DatabaseName = DATABASE_NAME, TableName = TB_NAME, MaxResults = MAX_RESULTS,Expression = "CreationTime < '2019-12-06'")

response = client.get_partitions(DatabaseName = DATABASE_NAME, TableName = TB_NAME, MaxResults = MAX_RESULTS, Expression = " path_name < '2019-12-11' " )

print((response['Partitions']))
print(len(response['Partitions']))

#print((response['Partitions'][0]['CreationTime']))

# https://docs.aws.amazon.com/cli/latest/reference/glue/get-partitions.html
#  filter the partition values using  get-partitions --expression(as per your use-case)
# and pass the values to the batch_delete_partition to delete the filtered partitions.

# Get values based on Creation time.
# 'CreationTime': datetime.datetime(2019, 12, 10, 20, 17, 29, tzinfo=tzlocal())

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
#execute_glue_api(DATABASE_NAME,TB_NAME,part_list)

'''
{
   "CatalogId": "string",
   "DatabaseName": "string",
   "Expression": "string",
   "MaxResults": number,
   "NextToken": "string",
   "Segment": {
      "SegmentNumber": number,
      "TotalSegments": number
   },
   "TableName": "string"
}
'''

print(datetime.now() - startTime)
