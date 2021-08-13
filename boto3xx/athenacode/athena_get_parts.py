"""
Athena partitioning script
"""


import os
import sys
import time
import random
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import csv
import json
import re
import urllib.request
import boto3
from dateutil.relativedelta import relativedelta
from botocore.config import Config
from botocore.exceptions import ClientError

# Change the profile of the default session in code
boto3.setup_default_session(profile_name='prod')

ATHENA_LOG = 's3-dq-athena-log-prod'
PATTERN = re.compile("20[0-9]{2}-[0-9]{1,2}-[0-9]{1,2}")
TWOMONTHSPLUSCURRENT = ((datetime.date.today() - relativedelta(months=2)).replace(day=1) - datetime.timedelta(days=1))
THIRTYDAYS = (datetime.date.today() - datetime.timedelta(days=30))
TODAY = datetime.date.today()
LOG_FILE = "/tmp/athena-partition.log"

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
CONSOLEHANDLER = logging.StreamHandler()
CONSOLEHANDLER.setFormatter(FORM)
LOGGER.addHandler(CONSOLEHANDLER)
LOGGER.info("Starting")

LOG_GROUP_NAME = None
LOG_STREAM_NAME = None


CONFIG = Config(
    retries=dict(
        max_attempts=10
    )
)

S3 = boto3.client('s3', region_name='eu-west-2') # Can we have S3 specific Config?
ATHENA = boto3.client('athena', config=CONFIG, region_name='eu-west-2')
GLUE = boto3.client('glue', config=CONFIG , region_name='eu-west-2')

def error_handler(lineno, error):
    """
    Error Handler
    Can submit Cloudwatch events if LOG_GROUP_NAME and LOG_STREAM_NAME are set.
    """

    LOGGER.error('The following error has occurred on line: %s', lineno)
    LOGGER.error(str(error))
    sess = boto3.session.Session(profile_name='prod')
    region = sess.region_name
    #region_name

    raise Exception("https://{0}.console.aws.amazon.com/cloudwatch/home?region={0}#logEventViewer:group={1};stream={2}".format(region, LOG_GROUP_NAME, LOG_STREAM_NAME))



def clear_down(sql):
    """
    After an Athena failure, delete the target path before the sql is retried
    Args:
        sql         : the SQL to execute
    Returns:
        None
    """

    try:
        full_path = sql.split('s3://')[1].split("'")[0]
        bucket_name = full_path.split('/')[0]
        path_to_delete = '/'.join(full_path.split('/')[1:])

        LOGGER.info(
            'Attempting to delete %s from bucket %s',
            path_to_delete,
            bucket_name)

        bucket = S3.Bucket(bucket_name)
        response = bucket.objects.filter(Prefix=path_to_delete).delete()
        LOGGER.info(response)

        if not response:
            LOGGER.info('Nothing to delete')
        else:
            LOGGER.info('The following was deleted: %s', response[0]['Deleted'])

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def check_query_status(execution_id):
    """
    Loop until the query is either successful or fails
    Args:
        execution_id             : the submitted query execution id
    Returns:
        None
    """
    try:
        client = boto3.client('athena', config=CONFIG ,region_name='eu-west-2')
        LOGGER.debug('About to check Athena status on SQL')
        while True:
            response = client.get_query_execution(
                QueryExecutionId=execution_id)
            if response['QueryExecution']['Status']['State'] in ('FAILED', 'SUCCEEDED', 'CANCELLED'):
                return response
            LOGGER.debug('Sleeping for 1 second')
            time.sleep(1)

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

# new addition

# new addition

def create_partitions(data, database_name, table_name):

    break_list_in_chunks = lambda data, chunk: [data[x:x+chunk] for x in range(0, len(data), chunk)]

    for i, data in enumerate(break_list_in_chunks(data, 100)):
        print(i)
        create_partition_response = GLUE.batch_create_partition(
                DatabaseName=database_name,
                TableName=table_name,
                PartitionInputList=data
            )
            
# new addition
def get_partitions(database, table):
    """
    Loop until the query is either successful or fails
    Args:
        execution_id             : the submitted query execution id
    Returns:
        None
    """
    try:
        #gluesession = boto3.Session(profile_name='prod')
        #glue_client = gluesession.client("glue", "eu-west-2")

        kwargs = {
            'DatabaseName' : database,
            'TableName' : table,
            'MaxResults' : 999,
            }

        while True:
            resp = GLUE.get_partitions(**kwargs)
            yield from resp['Partitions']
            try:
                kwargs['NextToken'] = resp['NextToken']
            except KeyError as err:
                break
    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

# new addition
def execute_glue_api_delete(database_name, tb_name, partition_val):
    """
    Function that calls glue's batch delete partition API.
    """
    try:

        GLUE.batch_delete_partition(DatabaseName=database_name, TableName=tb_name, PartitionsToDelete=partition_val)
        print("Dropped:", partition_val)
    except ClientError as err:
        if err.response['Error']['Code'] in 'EntityNotFoundException':
            err = 'Table ' + database_name + '.' + tb_name + ' partitions'  + ' not found!'
            LOGGER.warning(err)
        else:
            error_handler(sys.exc_info()[2].tb_lineno, err)

def execute_athena(sql, database_name):
    """
    Run SQL on Athena.
    Args:
        sql             : the SQL to execute
        conditions      : dict of optional pre and post execution conditions
        output_location : the S3 location for Athena to put the results
    Returns:
        response        : response of submitted Athena query
    """


    try:
        attempts = 8
        i = 1
        while True:
            if i == attempts:
                LOGGER.error('%s attempts made. Failing with error', attempts)
                sys.exit(1)
            try:
                response = ATHENA.start_query_execution(
                    QueryString=sql,
                    QueryExecutionContext={
                        'Database': database_name
                        },
                    ResultConfiguration={
                        'OutputLocation': "s3://" + ATHENA_LOG,
                        }
                    )
            except ClientError as err:
                if err.response['Error']['Code'] in (
                        'TooManyRequestsException',
                        'ThrottlingException',
                        'SlowDown'):
                    LOGGER.info('athena.start_query_execution throttled. Waiting %s second(s) before trying again', 2 ** i)
                    time.sleep((2 ** i) + random.random())
                else:
                    raise err
                i += 1
            else:
                LOGGER.debug('Athena query submitted. Continuing.')
                LOGGER.debug(response)
                response = check_query_status(response['QueryExecutionId'])
                if response['QueryExecution']['Status']['State'] == 'CANCELLED':
                    LOGGER.warning(response)
                    LOGGER.debug('SQL query cancelled. Waiting %s second(s) before trying again', 2 ** i)
                    time.sleep((2 ** i) + random.random())
                    i += 1
                    clear_down(sql)
                if response['QueryExecution']['Status']['State'] == 'FAILED':
                    LOGGER.warning(response)
                    state_change_reason = response['QueryExecution']['Status']['StateChangeReason']
                    compiled = re.compile("Table*does not exist")
                    compiled_not_found = re.compile("Table not found*")
                    if "Query exhausted resources at this scale factor" in state_change_reason \
                       or "Partition metadata not available" in state_change_reason \
                       or "INTERNAL_ERROR" in state_change_reason \
                       or "ABANDONED_QUERY" in state_change_reason \
                       or "HIVE_PATH_ALREADY_EXISTS" in state_change_reason \
                       or "HIVE_CANNOT_OPEN_SPLIT" in state_change_reason \
                       or compiled.match(state_change_reason) \
                       or compiled_not_found.match(state_change_reason):
                        LOGGER.debug('SQL query failed. Waiting %s second(s) before trying again', 2 ** i)
                        time.sleep((2 ** i) + random.random())
                        i += 1
                        clear_down(sql)
                    if "Table not found" in state_change_reason:
                        LOGGER.warning('Database / Table not found, continuing.')
                        LOGGER.warning(sql)
                        sys.exit(1)
                    else:
                        LOGGER.error('SQL query failed and this type of error will not be retried. Exiting with failure.')
                        sys.exit(1)
                elif response['QueryExecution']['Status']['State'] == 'SUCCEEDED':
                    LOGGER.debug('SQL statement completed successfully')
                    break

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

    return response

def partition(database_name, table_name, s3_location, retention, drop_only):
    """
    Gets a list of partitions from Athena, then removes partitions based on the retention period.
    Args:
        database_name  : the schema name in Athena
        table_name     : the table name in Athena
        s3_location    : the S3 location of the data in the schema
        retention      : retention period / days to keep
    Returns:
        None
    """

    try:
        LOGGER.info('Processing %s.%s, removing partitions older than %s.', database_name, table_name, retention)

        sql = "show partitions " + database_name + "." + table_name

        response = execute_athena(sql, database_name)
        execution_id = response['QueryExecution']['QueryExecutionId']

        query_results = ATHENA.get_query_results(
            QueryExecutionId=execution_id)

        partition_list = []

        #new addition
        for parts in get_partitions(database_name, table_name):
            #print(parts["StorageDescriptor"])
            #print(parts["StorageDescriptor"]["Location"])
            #print(parts["Values"])


            # Add Partitions to archive table if applicable.
            archive_table_name = table_name + '_archive'

            # Let us iterate 25 at a time.

            for idx,vals in enumerate(parts["Values"]):
                #print(vals)
                try:
                    match = PATTERN.search(vals).group(0)
                    #print(f'match is {match}')
                    if match <= str(retention):
                        glue_partition_list = [{'Values': [vals]}]
                        if(not drop_only):
                            #create partitions. 25 at a time.
                            #create_partitions(glue_partition_list, database_name, table_name)

                        #execute_glue_api_delete(database_name, table_name, glue_partition_list)
                        print(glue_partition_list)

                except:
                    LOGGER.info(f"No match found")
                    break # why this break



        for row in query_results['ResultSet']['Rows']:
            path_name = row['Data'][0]['VarCharValue']
            #print("*"*50)
            #print(f'Path name from Athena result {path_name}')
            # Path name from Athena result path_name=2020-09-01/10:10:10.814904-consolidated
            try:
                match = PATTERN.search(path_name).group(0)
                #print("-"*50)
                #print(f' Match is {match} and path_name is {path_name}')
                #Match is 2020-08-04 and path_name is path_name=2020-08-04/180019
                break
                #Match is 2020-09-01
                if match <= str(retention):
                    if path_name.startswith('path_name='):
                        partition_list.append(path_name)
                    else:
                        partition_list.append("""path_name={0}""".format(path_name))
            except:
                LOGGER.info("No match found.")
                break # why this break

        for item in partition_list:
            item_quoted = item[:10] + "'" + item[10:] + "'"
            item_stripped = item.split('=')[1]

            drop_partition_sql = ("ALTER TABLE " + database_name + "." + table_name + \
                                 " DROP PARTITION (" + item_quoted + ");")
            add_partition_sql = ("ALTER TABLE " + database_name + "." + table_name + \
                                 "_archive ADD PARTITION (" + item_quoted + ") LOCATION 's3://" + s3_location + "/" + item_stripped + "';")

            #print(drop_partition_sql)
            #print(add_partition_sql)

        LOGGER.info("Complete.")

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


if __name__ == '__main__':
    database_name='internal_reporting_prod'
    table_name='dim_parsed_message'
    s3_location='s3-dq-reporting-internal-working-prod/dim_parsed_message/storage'
    #retention = str(TWOMONTHSPLUSCURRENT)
    retention = str(THIRTYDAYS)
    drop_only=False
    partition(database_name, table_name, s3_location, retention, drop_only)
