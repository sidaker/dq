import boto3
import pprint
import datetime

glue = boto3.client('glue', region_name='eu-west-2')
client = boto3.client('s3',region_name = 'eu-west-2')
d1 = datetime.datetime(2019, 10, 31).date()
d2 = datetime.datetime(2020, 02, 07).date()

# Grab all partitions for the table
results = glue.get_partitions(
    DatabaseName=glue_database,
    TableName='internal_storage_by_std_date_local'
        )
# Loop through the results
for key in results['Partitions']:
    partitiondate = datetime.datetime.strptime(key['Values'][1],  '%Y-%m-%d %H:%M:%S').date()
    if partitiondate >= d1 and partitiondate <= d2:
        # If the key matches the first partition value that we are after
        print('Found an example with location ' + key['StorageDescriptor']['Location'])
        # Method cuts off starting ':' in 's3://'  so it isn't replaced with '%3a'
        key['StorageDescriptor']['Location'] = 's3://' + key['StorageDescriptor']['Location'][5:].replace(':', '%3A')
        print('New Location: ' + key['StorageDescriptor']['Location']);
        # Remove keys which can't be used as input as these will cause exceptions
        del key['TableName']
        del key['DatabaseName']
        del key['CreationTime']
        print("Updating with the following input")
        pprint.pprint(key)
        s3_path = key['StorageDescriptor']['Location'].split('/')
        bucket_name = s3_path[2]
        s3_prefix = "/".join(s3_path[3:]) + "/"
        print("s3_prefix: " + s3_prefix)
        response = client.list_objects_v2(Bucket=bucket_name, Delimiter='/', MaxKeys=1, Prefix=s3_prefix)
        if 'Contents' in response:
            glue.update_partition(
                DatabaseName=glue_database,
                TableName='internal_storage_by_std_date_local',
                PartitionValueList=key['Values'],
                PartitionInput=key
                    )
        else:
            print("S3 path is not valid")
