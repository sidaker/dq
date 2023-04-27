import boto3


def get_matching_s3_objects(bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3session = boto3.Session(profile_name='prod')
    s3 = s3session.client("s3", "eu-west-2")
    #s3 = boto3.client("s3")
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


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj["Key"]

    def download_froms3(myfile, env='prod'):
        # session = boto3.Session(profile_name=PROFILE)
        boto_s3_session = boto3.Session(profile_name=env)
        s3 = boto_s3_session.resource('s3')
        s3client = boto_s3_session.client('s3', region_name='eu-west-2')
        try:
            file_name = unquote(myfile.split('/')[-1])
            oparse = urlparse(myfile, allow_fragments=False)
            print(oparse)
            S3_SRC_BUCKET_NAME = oparse.netloc
            key = oparse.path[1:]
            download_path = '{0}{1}'.format(BASE_PATH, file_name)
            print(f'Downloading  from {S3_SRC_BUCKET_NAME} , {key} to {download_path} ')
            # s3.Bucket(S3_SRC_BUCKET_NAME).download_file(key, download_path)
            # s3.Bucket(S3_SRC_BUCKET_NAME).download_file(file_name, download_path)
            s3client.download_file(S3_SRC_BUCKET_NAME, key, download_path)
            print('File Downloaded')
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == "404":
                print("The object does not exist.", err)
            else:
                # raise
                error = str(err)
                print(error)

        return myfile

if __name__ == '__main__':
    bucket_name = 's3-dq-acl-archive-prod'
    key = '2022-02-02/00:01:09.134721'

    '''
    for i in get_matching_s3_objects(bucket_name,suffix='.CSV'):
        print(i['Key'])
        print(i)
        
    for key in get_matching_s3_keys('s3-dq-acl-archive-prod',prefix='2022-02-02/00:01:09.134721/', suffix='.CSV'):
        print(key)    
    '''

    for key in get_matching_s3_keys('s3-dq-acl-archive-prod',prefix='2022-02', suffix='.CSV'):
        print(key)
        print("Copying to Notprod")
