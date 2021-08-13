import boto3
# SHOW TABLES IN reference_data_notprod 'input_file_*'
ath_db ='reference_data_notprod'
sessprofile='notprod'
boto3.setup_default_session(profile_name=sessprofile)
client = boto3.client('athena', region_name='eu-west-2')

filepath = '/Users/sbommireddy/Downloads/table_list.csv'
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
                                               QueryExecutionContext={'Database': ath_db},
                                               ResultConfiguration={'OutputLocation': 's3://s3-dq-athena-log-notprod/working/default-output/'})


response = client.start_query_execution(QueryString=" SHOW TABLES IN reference_data_notprod 'input_file_*' ",
                                        QueryExecutionContext={'Database': ath_db},
                                        ResultConfiguration={'OutputLocation': 's3://s3-dq-athena-log-notprod/working/default-output/'})
query_execution_id = response['QueryExecutionId']
print (query_execution_id)
