import boto3

session = boto3.Session(profile_name='prod')
glue_client = session.client("glue", "eu-west-2")


def get_and_delete_partitions(database, table, batch=25):
    partitions = glue_client.get_partitions(
        DatabaseName=database,
        TableName=table)["Partitions"]

    print(len(partitions))

    for i in range(0, len(partitions), batch):
        to_delete = [{k:v[k]} for k,v in zip(["Values"]*batch, partitions[i:i+batch])]
        print(to_delete)


database='api_input_prod'
table='input_file_api'
get_and_delete_partitions(database, table, 25)
