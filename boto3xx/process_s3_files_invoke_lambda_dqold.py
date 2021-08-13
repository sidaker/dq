import boto3
import os
from datetime import datetime
import pytz
import json



def get_matching_s3_objects(bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")

    kwargs = {'Bucket': bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix, )
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = key_prefix

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                break

            for obj in contents:
                key = obj["Key"]
                lmd =  obj["LastModified"]
                utc=pytz.UTC
                lower_cutoffdt = utc.localize(datetime.strptime('2020-07-30 10:46:31', '%Y-%m-%d %H:%M:%S'))
                upper_cutoffdt = utc.localize(datetime.strptime('2020-07-30 10:47:58', '%Y-%m-%d %H:%M:%S'))
                #print(lmd)
                if key.endswith(suffix) and lmd > lower_cutoffdt and lmd < upper_cutoffdt:
                    yield obj


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        #yield obj["Key"]
        yield obj


if __name__ == '__main__':
    #env='notprod'
    env='prod'
    #env='default'
    namespace = 'prod'
    triggerlambda=f'arn:aws:lambda:eu-west-2:337779336338:function:acl-input-prod-lambda-trigger'
    # export AWS_DEFAULT_REGION=us-west-2
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    bucket_name = 's3-dq-api-archive-prod'

    for reprocessobj in get_matching_s3_keys(bucket_name, "parsed/2020-07-30/", "zip"):
        # Contruct event. payload accepts bytes.
        #print(reprocessobj)
        #exit()

        payload3 = json.dumps({
            "Records":[{
                "s3":{
                    "bucket":{
                        "name":bucket_name
                        },
                    "object":{
                        "key": reprocessobj['Key'],
                        "size": reprocessobj['Size'],
                        "eTag": reprocessobj['ETag']

                        }
                            }
                        }]
                    })
        #print(reprocesskey)
        #print(payload3['Records'][0]['s3']['bucket']['name'])
        #print(payload3['Records'][0]['s3']['object']['key'])

        #Trigger lambda
        client = boto3.client('lambda')

        response = client.invoke(
        FunctionName=triggerlambda,
        InvocationType='Event',
        LogType='None',
        ClientContext='triggeringfromdocker',
        Payload=payload3)

        try:

            response = client.invoke(
            FunctionName=triggerlambda,
            InvocationType='Event',
            LogType='None',
            ClientContext='triggeringfromdocker',
            Payload=payload3)
            print("****")
            print(response)

            #Introduce Wait. Don't trigger the next event immediately

        except:
            print("Error Occured")


# client = boto3.client('lambda')
# response = client.invoke(FunctionName='string',
# InvocationType='Event'|'RequestResponse'|'DryRun',
#  LogType='None'|'Tail',
#  ClientContext='string',
#  Payload=b'bytes'|file,
#  Qualifier='string')
