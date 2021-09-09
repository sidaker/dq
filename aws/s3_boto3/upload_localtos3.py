import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

local_file='/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises/data/test.csv'
bucket_name='s3-dq-test-prac-1'
s3_file_name='test/test.csv'
local_file_avro = '/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises/data/city.avro'
uploaded = upload_to_aws(local_file, bucket_name, s3_file_name)
uploaded = upload_to_aws(local_file_avro, bucket_name, 'test/newfile.avro')
