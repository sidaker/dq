import boto3
import time


def tictoc(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        elapsed = time.time() — start
        print(elapsed)

    return wrapper


class FindS3File(object):
    def __init__(
            self,
            bucket,
            pattern
    ):
        '''
        bucket <string>: S3 Bucket Name
        pattern <string>: String Pattern to match
        '''
        self.bucket = bucket
        self.pattern = pattern
        self.keys = []
        self.start_s3_client()
        self.get_s3_objects()
        self.show_keys_matching_pattern(self.pattern)

    def start_s3_client(
            self
    ):
        self.s3 = boto3.client('s3')

    def get_s3_objects(
            self
    ):
        paginator = self.s3.get_paginator("list_objects_v2")
        self.objects = paginator.paginate(
            Bucket=self.bucket
        )

    @tictoc
    def show_keys_matching_pattern(
            self,
            pattern
    ):
        for object in self.objects.search(f'Contents[?contains[Key, `{pattern}`)]'):
            try:
                self.keys.append(object['Key'])
            except Exception as err:
                print(f'Error with {object["Key"]}')


## main
def test():
    bucket = 's3://s3-dq-acl-archive-prod/2022-02-02/00:01:09.134721/'
    pattern = 'CSV'

    found = FindS3File(
        bucket=bucket,
        pattern=pattern
    )
    found.keys

if __name__ == '__main__':
    test()
