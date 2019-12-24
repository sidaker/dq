'''
Basic Python Code that bulk deletes partitions.
'''
import boto3
client = boto3.client('glue')

response = client.batch_delete_partition(
    CatalogId='**********',
    DatabaseName='sampledb',
    TableName='elb_logs_pq',
    PartitionsToDelete=[
            {'Values': ['2015','1','7']},
            {'Values': ['2015','1','8']},
            {'Values': ['2015','1','9']},
            {'Values': ['2015','1','10']},
            {'Values': ['2015','1','11']},
            {'Values': ['2015','1','12']},
            {'Values': ['2015','1','13']},
            {'Values': ['2015','1','14']},
            {'Values': ['2015','1','15']},
    ]
)
