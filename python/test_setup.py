import shutil
import boto3
import os
from os import path
import random
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from botocore.config import Config
from botocore.exceptions import ClientError

'''
Arguments:
    project:
    localbasedir:
    in_s3bucket:
    in_keypattern:

Usage:
  python test_setup.py
'''

'''
Steps:
1. Create Folders on Local directory for each test.
    - n folders are created for n test cases.
2. Inside each test case folder, create sub folders.
    - create sub folders
3. Download files from S3 to input subfolder of each test case
4. Sync directories with target s3.(pending implementation)
5. Alternatively copy from S3 to S3, instead of step 3 and 4.(pending implementation)
6. Create Config files and sync or upload them to S3 (Pending implementation)
'''

def download_from_s3(bucket_name, prefix, lpath):
    # download
    attempts = 4
    i = 1
    try:
        while True:
            if i == attempts:
                LOGGER.error('%s attempts made. Failing with error', attempts)
                sys.exit(1)
            try:
                #print(f"Attempting Download of {prefix} from {bucket_name} to {lpath} ")
                S3.download_file(bucket_name, prefix, lpath)
                #print("Downloaded")
            except ClientError as err:
                error_code = err.response['Error']['Code']
                if error_code == "404":
                    err = "Key not found in S3: " + bucket_name + "/" + prefix
                    print(err)
                    LOGGER.error(err)
                    sys.exit(1)
                else:
                    raise err
                i += 1
            else:
                LOGGER.info('Successfully Downloaded File')
                break
    except Exception as err:
        print(err)
        LOGGER.error('Unknown Error')


def prefix_exists(bucket_name, prefix):
    """
    If the prefix exists in the bucket / location, return True otherwise False
    """
    try:
        #print("Checking Prefix")
        result = False
        client = boto3.client('s3', config=CONFIG)
        response = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )
        # print(response)
        if response.get('Contents'):
            LOGGER.info('%s exists in %s.',
                           prefix,
                           bucket_name)
            result = True
        else:
            LOGGER.info('%s does not exist in %s.',
                        prefix,
                        bucket_name)
        return result

    except Exception as err:
        print(err)
        LOGGER.error('Unknown Error while checking %s in bucket %s.',
                    prefix,
                    bucket_name)

def dir_exists(path2):
    '''
        Check if Directory exists on the local machine
    '''
    return path.isdir(path2)


def path_exists(path2):
    '''
        Check if path exists on the local machine
    '''
    return path.exists(path2)


def check_dir_create(path2):
    if not os.path.exists(path2):
        os.makedirs(path2)


if __name__ == '__main__':

    basedir = '/Users/sbommireddy/Documents/testdownload'
    projectname = 'proj1'
    numberoftests = 7
    input_bucket_name = 's3-dq-accuracy-score-notprod'
    # s3://s3-dq-accuracy-score-notprod/2020-04-05/095029/20200405_095054_00006_x9mvm_7924f8b2-bc48-40e6-ae0c-f94f21aac524
    input_prefix = '2020-04-05/095029/20200405_095054_00006_x9mvm_7924f8b2-bc48-40e6-ae0c-f94f21aac524'
    LOG_FILE = "/Users/sbommireddy/Documents/testdownload/athena-partition.log"

    boto3.setup_default_session(profile_name='notprod')

    testdir = os.path.join(basedir, projectname)
    print(testdir)
    print("*"*50)
    """
    Setup Logging
    """
    LOGFORMAT = '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'
    FORM = logging.Formatter(LOGFORMAT)
    logging.basicConfig(
        format=LOGFORMAT,
        level=logging.INFO
        )

    LOGGER = logging.getLogger()
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGHANDLER = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=7)
    LOGHANDLER.suffix = "%Y-%m-%d"
    LOGHANDLER.setFormatter(FORM)
    LOGGER.addHandler(LOGHANDLER)

    CONFIG = Config(
    retries=dict(max_attempts=10)
        )

    S3 = boto3.client('s3')

    # create test dir under base dir if it does not exist.
    check_dir_create(testdir)

    # Create test case directories if they dont exist.
    for i in range(numberoftests):
        print(f'Creating Test Case directory:{i+1}')
        testcasedir = os.path.join(testdir, 'testcase_' + str(i+1) )
        check_dir_create(testcasedir)

        #create directories for input, output, error, archive, datalake
        for dire in ['input', 'output', 'error', 'archive', 'datalake']:
            subdir = os.path.join(testcasedir, dire )
            check_dir_create(subdir)


            # Download .OK and file from s3 into input
            if(dire == 'input'):
                print("-"*50)
                filename = input_prefix.split("/")[-1]
                lpath = os.path.join(subdir, filename )
                #okfile = lpath + ".ok"
                if prefix_exists(input_bucket_name, input_prefix):
                    # proceed only if key exists.
                    print(f'{input_prefix} in bucket {input_bucket_name} \
exists. Downloading to {lpath}.')
                    download_from_s3(input_bucket_name, input_prefix, lpath)
                    # download_from_s3(input_bucket_name, input_prefix, okfile)



    # Create Config file based on template.
