import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
print('Existing buckets:')
for bucket in s3.buckets.all():
    print(bucket.name)
