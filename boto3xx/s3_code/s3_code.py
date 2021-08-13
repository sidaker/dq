import boto3
import json

BUCKET_NAME =  'dq-test-del-my-bucket'

def s3_client():
    s3 = boto3.client('s3',region_name='eu-west-2')
    ''' type <class 'botocore.client.S3'> '''
    #print(type(s3))
    return s3


def create_bucket(BUCKET_NAME):
    return s3_client().create_bucket(
        Bucket= BUCKET_NAME,
        CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-2'
            }
    )

# use https://awspolicygen.s3.amazonaws.com/policygen.html
# Below will generate a policy with public access to the bucket whcih is not advised
def create_bucket_policy(BUCKET_NAME):
    # create a dictionary called bucket_policy
    bucket_policy = {
        "Id": "Policy1583150292905",
        "Version": "2012-10-17",
        "Statement": [
            {
            "Sid": "Allow Permissions",
            "Action": "s3:*",
            "Effect": "Allow",
            "Resource": "arn:aws:s3:::" + BUCKET_NAME + "/*",
            "Principal": "*"
            }
        ]
    }

    # Convert the dictionary to json.
    policy_string = json.dumps(bucket_policy)

    return s3_client().put_bucket_policy(
        Bucket= BUCKET_NAME,
        Policy = policy_string
    )

def list_buckets():
    return s3_client().list_buckets()

def get_bucket_policy(BUCKET_NAME):
    return s3_client().get_bucket_policy(Bucket= BUCKET_NAME)

def get_bucket_encryption(BUCKET_NAME):
    return s3_client().get_bucket_encryption(Bucket= BUCKET_NAME)


def update_bucket_policy(BUCKET_NAME):
    # create a dictionary called bucket_policy
    bucket_policy = {
        "Id": "Policy1583150292905",
        "Version": "2012-10-17",
        "Statement": [
            {
            "Sid": "Allow Permissions",
            "Action": "s3:*",
            "Effect": "Allow",
            "Resource": "arn:aws:s3:::" + BUCKET_NAME + "/*",
            "Principal": "*"
            }
        ]
    }

    # Convert the dictionary to json.
    policy_string = json.dumps(bucket_policy)

    return s3_client().put_bucket_policy(
        Bucket= BUCKET_NAME,
        Policy = policy_string
    )

def server_side_encryption():
    return s3_client().put_bucket_encryption(
            Bucket= BUCKET_NAME,
            ServerSideEncryptionConfiguration = {
                'Rules' : [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'aws:kms',
                            'KMSMasterKeyID':
                            'arn:aws:kms:eu-west-2:093401982388:key/719c7b3f-addd-4165-bd4b-c3dcdc676dc7'
                            }
                    }


                ]
            }
    )


if __name__ == '__main__':
    print(create_bucket(BUCKET_NAME))
    print(create_bucket_policy(BUCKET_NAME))
    #print(list_buckets())
    #print(list_buckets()['Buckets'][0]['Name'])
    #print(get_bucket_policy('aws-account-provisioner-093401982388'))
    #print(get_bucket_policy('aws-account-provisioner-093401982388')['Policy'])
    #print(get_bucket_encryption('aws-account-provisioner-093401982388'))
    #print(get_bucket_encryption('aws-account-provisioner-093401982388')['ServerSideEncryptionConfiguration']['Rules'])
    #print(update_bucket_policy(BUCKET_NAME))
    print(server_side_encryption())
