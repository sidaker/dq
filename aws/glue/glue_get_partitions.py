import boto3
import pprint

session = boto3.Session(profile_name='notprod')
glue = session.client('glue', region_name='eu-west-2')


# Grab all partitions for the table
results = glue.get_partitions(
    DatabaseName='api_cross_record_scored_notprod',
    TableName='internal_storage_by_std_date_local_recent'
        )

for ct,key in enumerate(results['Partitions']):
    print(key['Values'])
    if(ct>9) :
        break


'''
hodqadms-MacBook-Pro:glue sbommireddy$ python glue_get_partitions.py
['2020-04-16', '2020-04-16 14:50:41']
['2019-12-02', '2019-12-05 11:50:17']
['2019-12-04', '2019-12-06 11:50:19']
['2020-02-03', '2020-02-04 11:50:18']
['2020-02-03', '2020-02-06 12:20:50']
['2019-12-17', '2019-12-19 11:50:18']
['2020-02-02', '2020-02-04 11:50:18']
['2019-12-11', '2019-12-11 11:50:24']
['2019-12-11', '2019-12-13 11:50:18']
['2020-04-16', '2020-04-17 11:51:06']
['2020-01-01', '2020-01-02 11:50:16']
hodqadms-MacBook-Pro:glue sbommireddy$ pwd
/Users/sbommireddy/Documents/python/assignments/dq/aws/glue
'''
