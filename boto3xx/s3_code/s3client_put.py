import boto3

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

## s3-dq-api-archive-test

putmessage = b'Let us put this data to s3'

## put object

response = s3_client.put_object(
    Body = putmessage,
    Bucket = 's3-dq-api-archive-test',
    Key = 'testboto3put.txt'
)


print(response)

## Copy

toCopy = {
    'Bucket': 's3-dq-api-archive-test',
    'Key': 'testboto3put.txt'
}

## make a copy
s3_resource.meta.client.copy(toCopy, 's3-dq-api-archive-test', 'copytestboto3put.txt' )

## another way to copy
response = s3_client.copy_object(
    Bucket = 's3-dq-api-archive-test',
    CopySource = 's3-dq-api-archive-test/testboto3put.txt',
    Key = 'testboto3copyobj.txt'
)