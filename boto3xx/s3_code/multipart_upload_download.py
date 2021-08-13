import boto3
from boto3.s3.transfer import TransferConfig
import os
import threading
import sys

'''
Amazon Simple Storage Service (S3) can store files up to 5TB, yet with a single PUT operation,
we can upload objects up to 5 GB only.
Amazon suggests, for objects larger than 100 MB, customers should consider using the Multipart Upload capability.
'''

'''
When uploading, downloading, or copying a file or S3 object, the AWS SDK for Python
automatically manages retries, multipart and non-multipart transfers.
In order to achieve fine-grained control, the default settings can be configured
to meet requirements. TransferConfig object is used to configure these settings.
The object is then passed to a transfer method (upload_file, download_file) in the Config= parameter.
'''

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()


    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()




def multipart_download_boto3(s3_resource, file_path, key, bucket_name, config, progresspath):

    #file_path = os.path.dirname(__file__)+ '/AWS_SYSOPS_COOKBOOK_SECOND.pdf'
    print(f'Begin Download to...{file_path}')
    print(f'Progress to...{progresspath}')
    resp = s3_resource.Object(bucket_name, key).download_file(file_path,
                            Config=config,
                            Callback=ProgressPercentage(progresspath)
                            )
    print("End of Download")
    return resp


def multipart_upload_boto3(s3_resource, file_path, key, bucket_name, config):

    resp = s3_resource.Object(bucket_name, key).upload_file(file_path,
                            ExtraArgs={'ContentType': 'text/pdf'},
                            Config=config,
                            Callback=ProgressPercentage(file_path)
                            )
    return resp

if __name__ == '__main__':
    bucket_name = 's3-dq-rls-xrs-reconciliation-test'
    #file_path = os.path.dirname(__file__) + '/multipart_upload_example.pdf'
    #file_path1 = os.path.dirname(__file__)
    up_file_path = os.path.dirname('/Users/sbommireddy/Documents/Books/') + '/AWS_SYSOPS_COOKBOOK_SECOND.pdf'
    down_file_path = '/Users/sbommireddy/Documents/testdownload/file/' + '/multipart_download_example.pdf'
    lpath = '/Users/sbommireddy/Documents/testdownload/progress/'

    key = 'leftest/AWS_SYSOPS_COOKBOOK_SECOND.pdf'

    config = TransferConfig(multipart_threshold=1024 * 15,
                           max_concurrency=10,
                           multipart_chunksize=1024 * 10,
                           use_threads=True)

    s3_resource = boto3.resource('s3')

    print(multipart_upload_boto3(s3_resource, up_file_path,key,bucket_name, config))
    print("*"*50)
    print(multipart_download_boto3(s3_resource, down_file_path, key, bucket_name, config, lpath))



'''
multipart_threshold: This is used to ensure that multipart uploads/downloads only happen if the size of a transfer is larger than the threshold mentioned, I have used 25MB for example.
max_concurrency: This denotes the maximum number of concurrent S3 API transfer operations that will be taking place (basically threads). Set this to increase or decrease bandwidth usage.This attribute’s default setting is 10.If use_threads is set to False, the value provided is ignored.
multipart_chunksize: The size of each part for a multi-part transfer. Used 25MB for example.
use_threads: If True, parallel threads will be used when performing S3 transfers. If False, no threads will be used in performing transfers.
'''

'''
- file_path: location of the source file that we want to upload to s3 bucket.
- bucket_name: name of the destination S3 bucket to upload the file.
- key: name of the key (S3 location) where you want to upload the file.
- ExtraArgs: set extra arguments in this param in a json string. You can refer this link for valid upload arguments.
- Config: this is the TransferConfig object which I just created above.
https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/s3.html

'''
