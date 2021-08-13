import boto3
import os

# SHOW TABLES IN asn_maritime_test 'internal_storage_table_*_20210708*'
# Change the profile of the default session in code
env='dqtest'
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
session = boto3.Session(profile_name=env)
client = session.client('athena', region_name='eu-west-2')

#boto3.setup_default_session(profile_name='dqtest')
#client = boto3.client('athena', region_name='eu-west-2')

dbname = 'asn_maritime_test'
# "asn_maritime_test"."internal_storage_table_abmkhjobppaaknbhphkfdpifajfhohga_20210708_091640_100522"
print("Reading list of tables")
filepath = '/Users/sbommireddy/Downloads/int.csv'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       print("Line {}: {}".format(cnt, line.strip()))
       tablename1 = line.strip()
       #print(type(tablename1))

       line = fp.readline()
       cnt += 1
       query1 = 'DROP TABLE ' + tablename1
       print(query1)
       response = client.start_query_execution(QueryString=query1,
                                               QueryExecutionContext={'Database': dbname},
                                               ResultConfiguration={'OutputLocation': 's3://s3-dq-athena-log-test/working/default-output/'})


response = client.start_query_execution(QueryString="SHOW TABLES IN asn_maritime_test 'internal_storage_table_*_20210709**' ",
                                        QueryExecutionContext={'Database': dbname},
                                        ResultConfiguration={'OutputLocation': 's3://s3-dq-athena-log-test/working/default-output/'})
query_execution_id = response['QueryExecutionId']
print (query_execution_id)
