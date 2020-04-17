import boto3

session = boto3.Session(profile_name='notprod')
glue_client = session.client("glue", "eu-west-2")

database='api_cross_record_scored_notprod'
table='internal_storage_by_std_date_local_recent'

glue_client.batch_delete_partition(
    DatabaseName=database,
    TableName=table,
    PartitionsToDelete=[{'Values': ['2020-02-03', '2020-02-04 11:50:18']}])
