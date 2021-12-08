import boto3
import datetime
import pandas as pd
import time
import botocore
from urllib.parse import unquote
from urllib.parse import urlparse

BASE_PATH = '/Users/sbommireddy/Downloads/acl/data/'


def download_froms3(myfile,env='prod'):
        #session = boto3.Session(profile_name=PROFILE)
        boto_s3_session = boto3.Session(profile_name=env)
        s3 = boto_s3_session.resource('s3')
        s3client = boto_s3_session.client('s3', region_name='eu-west-2')
        try:
            file_name = unquote(myfile.split('/')[-1])
            oparse = urlparse(myfile, allow_fragments=False)
            print(oparse)
            S3_SRC_BUCKET_NAME = oparse.netloc
            key = oparse.path[1:]
            download_path = '{0}{1}'.format(BASE_PATH,file_name)
            print(f'Downloading  from {S3_SRC_BUCKET_NAME} , {key} to {download_path} ')
            #s3.Bucket(S3_SRC_BUCKET_NAME).download_file(key, download_path)
            #s3.Bucket(S3_SRC_BUCKET_NAME).download_file(file_name, download_path)
            s3client.download_file(S3_SRC_BUCKET_NAME,key,download_path)
            print('File Downloaded')
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == "404":
                print("The object does not exist." , err)
            else:
                #raise
                error = str(err)
                print(error)

        return myfile

def get_matching_s3_objects(bucket, prefix="", suffix="", env1=""):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    boto_s3_session = boto3.Session(profile_name=env1)
    s3 = boto_s3_session.client("s3")
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
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(bucket, prefix="", suffix="",env1="test"):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """

    for obj in get_matching_s3_objects(bucket, prefix, suffix, env1):
        yield obj["Key"]


if __name__ == '__main__':
    bucket_name = 's3-dq-acl-archive-prod'

    numdays = 10
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
    #print(date_list)
    #li1 = pd.date_range(start="2021-09-02",end="2021-09-14")
    li1 = pd.date_range(start="2021-09-02",end="2021-09-14").to_pydatetime().tolist()
    for dt in li1:
        dt1 =  dt.date().strftime("%Y-%m-%d")
        for key in get_matching_s3_keys(bucket_name,prefix=dt1, suffix='.CSV',env1='prod'):
            #print(key)
            fullpath='s3://'+bucket_name+'/' + key
            print(fullpath)
            download_froms3(fullpath)
