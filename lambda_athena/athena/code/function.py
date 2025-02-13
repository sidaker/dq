#pylint: disable=broad-except
"""
Main controller code for responding to events.
"""

import datetime
import time
import re
import json
import logging
import urllib.parse
import urllib.request
import uuid
import os
import random
import sys
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOG_GROUP_NAME = None
LOG_STREAM_NAME = None

CONFIG = Config(
    retries=dict(
        max_attempts=20
    )
)

def error_handler(lineno, error):

    LOGGER.error('The following error has occurred on line: %s', lineno)
    LOGGER.error(str(error))
    sess = boto3.session.Session()
    region = sess.region_name

    raise Exception("https://{0}.console.aws.amazon.com/cloudwatch/home?region={0}#logEventViewer:group={1};stream={2}".format(region, LOG_GROUP_NAME, LOG_STREAM_NAME))


def send_message_to_slack(text):
    """
    Formats the text provides and posts to a specific Slack web app's URL

    Args:
        text : the message to be displayed on the Slack channel

    Returns:
        Slack API repsonse
    """


    try:
        post = {
            "text": ":fire: :sad_parrot: *CRITICAL RLS Athena Pipleine Error - Needs immediate attention :sad_parrot: :fire:",
            "attachments": [
                {
                    "text": "{0}".format(text),
                    "color": "#B22222",
                    "attachment_type": "default",
                    "fields": [
                        {
                            "title": "Priority",
                            "value": "High",
                            "short": "false"
                        }
                    ],
                    "footer": "AWS",
                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
                }
            ]
            }

        ssm_param_name = 'slack_notification_webhook'
        ssm = boto3.client('ssm', config=CONFIG)
        try:
            response = ssm.get_parameter(Name=ssm_param_name, WithDecryption=True)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ParameterNotFound':
                LOGGER.info('Slack SSM parameter %s not found. No notification sent', ssm_param_name)
                return
            else:
                LOGGER.error("Unexpected error when attempting to get Slack webhook URL: %s", e)
                return
        if 'Value' in response['Parameter']:
            url = response['Parameter']['Value']

            json_data = json.dumps(post)
            req = urllib.request.Request(
                url,
                data=json_data.encode('ascii'),
                headers={'Content-Type': 'application/json'})
            LOGGER.info('Sending notification to Slack')
            response = urllib.request.urlopen(req)

        else:
            LOGGER.info('Value for Slack SSM parameter %s not found. No notification sent', ssm_param_name)
            return

    except Exception as err:
        LOGGER.error(
            'The following error has occurred on line: %s',
            sys.exc_info()[2].tb_lineno)
        LOGGER.error(str(err))

def prefix_exists(bucket_name, prefix):
    """
    AWS guarantee that an S3 event notification will be delivered at least once.
    If the prefix exists in the target bucket / location, the event is ignored
    """
    try:
        result = False
        client = boto3.client('s3', config=CONFIG)
        response = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )
        if response.get('Contents'):
            LOGGER.warning('%s exists in %s. Event ignored. Exiting.',
                           prefix,
                           bucket_name)
            result = True
        else:
            LOGGER.info('%s does not exist in %s. Continuing.',
                        prefix,
                        bucket_name)
        return result

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def upload_s3_object(local_file, bucket_name, key_name):
    """ upload local_file as key_name to bucket_name """

    try:
        s3_conn = boto3.resource('s3', config=CONFIG)
        s3_conn.Bucket(bucket_name).upload_file(local_file, key_name)
        LOGGER.info(
            '%s uploaded to %s as %s',
            local_file,
            bucket_name,
            key_name)

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def get_parameter(parameter_name):
    """
    Return a specific parameter value from config file..

    Args:
        parameter_name : parameter_name as per config file

    Returns:
        Parameter value
    """

    try:
        with open("transform/transform_config", 'r') as stream:
            content = stream.readlines()
            content = [x.strip() for x in content]
            config_dict = {}
            for line in content:
                sline = line.split('=')
                config_dict[sline[0]] = sline[1]
            if 'PATHMATCH' not in config_dict:
                LOGGER.warning('PATHMATCH not found, returning default config.')
                returnval = 'NOTFOUND'
            else:
                LOGGER.info('Parameter: %s ', parameter_name)
                LOGGER.info('Value: %s ', config_dict[parameter_name])
                returnval = config_dict[parameter_name]
            return returnval
    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def get_transform_dir(file_name):
    """
    Return the transform directory name based on the input file.

    Args:
        None

    Returns:
        Transform directory name
    """

    pathmatch = get_parameter('PATHMATCH')
    if pathmatch == 'NOTFOUND':
        return 'transform'
    else:
        pathmatch_elements = pathmatch.split(',')
        for element in pathmatch_elements:
            if element.split(':')[0] in file_name:
                return element.split(':')[1]
    LOGGER.info('Config not found, returning default.')
    return 'transform'

OUTPUT_BUCKET_NAME = os.environ['output_bucket_name']
GLUE_DATABASE = os.environ['glue_database']
NAMESPACE = os.environ['namespace']
VERSION = "0.3.2"

def get_sql_files(transform_dir):
    """
    Return a list of SQL files to run with Athena handling.

    The order of the list defines the order of execution.

    Args:
        None

    Returns:
        List of SQL filenames with paths relative to the Python code
    """

    transform_logic_path = '{0}/transform_logic'.format(transform_dir)
    LOGGER.info('transform_logic path: %s', transform_logic_path)
    sql_path = '{0}/sql/'.format(transform_dir)
    LOGGER.info('sql path: %s', sql_path)

    with open(transform_logic_path, 'r') as stream:
        try:
            content = stream.readlines()
            content = [sql_path + x.strip() for x in content if x[0] != '#']
            return content
        except Exception as err:
            error_handler(sys.exc_info()[2].tb_lineno, err)

def get_instance():
    """
    Return a randomly generated string which is used as a suffix
    in table names to guarantee uniqueness.

    Args:
        None

    Returns:
        Randomly generated string.
    """

    return (uuid.uuid4().hex.
            replace('0', 'g').
            replace('1', 'h').
            replace('2', 'i').
            replace('3', 'j').
            replace('4', 'k').
            replace('5', 'l').
            replace('6', 'm').
            replace('7', 'n').
            replace('8', 'o').
            replace('9', 'p'))


def table_exists_check(table_name):
    """
    Check if a table exists repeatedly and exit if it is not found after
    the configured number of attempts.

    Args:
       table_name   : table to check for, optionally prefixed with databasename.
    Returns:
       None, indicating table found,
         if the table is not found then the function will sys.exit(1)
    """

    glue = boto3.client('glue', config=CONFIG)
    if len(table_name.split('.')) == 2:
        database_name = table_name.split('.')[0]
        glue_table = table_name.split('.')[1]
    elif len(table_name.split('.')) == 1:
        database_name = GLUE_DATABASE
        glue_table = table_name
    else:
        LOGGER.error('table_name parameter %s is invalid. Failing.', table_name)
        sys.exit(1)

    attempts = 10
    i = 1
    while True:
        if i == attempts:
            LOGGER.error('%s attempts made. Failing with error', attempts)
            sys.exit(1)
        try:
            print('About to get table')
            response = glue.get_table(
                DatabaseName=database_name,
                Name=glue_table
            )
            LOGGER.debug(response)
            print('Got table')
        except ClientError as err:
            if err.response['Error']['Code'] == 'EntityNotFoundException':
                LOGGER.info(
                    '%s.%s not found. Waiting %s second(s) before trying again',
                    database_name,
                    glue_table,
                    2 ** i)
                time.sleep((2 ** i) + random.random())
            else:
                raise err
            i += 1
        else:
            LOGGER.info('%s.%s found. Continuing.', database_name, glue_table)
            break

def drop_partitions_athena(table_name, min_path_name, max_path_name, output_location, transform_dir, sql_params):
    """
    Drop partitions

    Args:
        table_name             : the table with partitions to drop
        min_path_name          : minimum path name to drop
        max_path_name          : maximum path name to drop
        output_location        : the S3 location for Athena to put the results
        transform_dir          : directory containing consolidation SQL
        sql_params             : parameters for substitution

    Returns:
        None
    """

    try:
        get_path_name_list_sql = """SELECT DISTINCT path_name FROM {0} WHERE path_name >= '{1}' AND path_name < '{2}'""".format(table_name, min_path_name, max_path_name)
        LOGGER.info('About to execute SQL:')
        LOGGER.info(get_path_name_list_sql)
        client = boto3.client('athena', config=CONFIG)

        sql_list = {}
        for sql_file in get_sql_files(transform_dir):
            (sql, conditions) = read_sql_file(sql_file,
                                              sql_params)
            conditions['pre_execution_table_exists_check'] = (
                substitute_params(conditions['pre_execution_table_exists_check'],
                                  sql_params))
            sql_list[sql_file] = sql
        # use same conditions value for all

        attempts = 8
        i = 1
        while True:
            if i == attempts:
                LOGGER.error('%s attempts made. Failing with error', attempts)
                sys.exit(1)
            try:
                response = client.start_query_execution(
                    QueryString=get_path_name_list_sql,
                    QueryExecutionContext={
                        'Database': GLUE_DATABASE
                    },
                    ResultConfiguration={
                        'OutputLocation': output_location
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
                LOGGER.info('Athena query submitted. Continuing.')
                LOGGER.info(response)
                execution_id = response['QueryExecutionId']
                response = check_query_status(response['QueryExecutionId'])
                if response['QueryExecution']['Status']['State'] == 'CANCELLED':
                    LOGGER.error(response)
                    LOGGER.error("The query was cancelled and will not be retried. Exiting with failure")
                    sys.exit(1)
                if response['QueryExecution']['Status']['State'] == 'FAILED':
                    LOGGER.warning(response)
                    state_change_reason = response['QueryExecution']['Status']['StateChangeReason']
                    compiled = re.compile("Table*does not exist")
                    if "Query exhausted resources at this scale factor" in state_change_reason \
                       or "Partition metadata not available" in state_change_reason \
                       or "INTERNAL_ERROR" in state_change_reason \
                       or "ABANDONED_QUERY" in state_change_reason \
                       or compiled.match(state_change_reason):
                        LOGGER.info('SQL query failed. Waiting %s second(s) before trying again', 2 ** i)
                        time.sleep((2 ** i) + random.random())
                        i += 1
                    else:
                        LOGGER.error('SQL query failed and this type of error will not be retried. Exiting with failure.')
                        sys.exit(1)
                elif response['QueryExecution']['Status']['State'] == 'SUCCEEDED':
                    LOGGER.info('SQL statement completed successfully with the following statistics:')
                    LOGGER.info(response['QueryExecution']['Statistics'])
                    if response['QueryExecution']['Statistics']['DataScannedInBytes'] < conditions['min_scan_bytes']:
                        LOGGER.error('DataScannedInBytes is below expected minimum %s.',
                                     conditions['min_scan_bytes'])
                        LOGGER.error('Exiting with failure')
                        sys.exit(1)
                    break

        LOGGER.info('About to get Athena results SQL')
        query_results = client.get_query_results(
            QueryExecutionId=execution_id)
        path_name_list = []
        simple_name_list = []
        for row in query_results['ResultSet']['Rows']:
            path_name_target = row['Data'][0]['VarCharValue']
            if path_name_target != 'path_name':
                path_name_list.append("""PARTITION (path_name = '{0}')""".format(path_name_target))
                simple_name_list.append(path_name_target)
        LOGGER.info(path_name_list)
        if path_name_list:
            sql_params['path-name-list'] = '\',\''.join(simple_name_list)
            LOGGER.info(sql_params['path-name-list'])
            for sql_file in get_sql_files(transform_dir):
                (sql, conditions) = read_sql_file(sql_file,
                                                  sql_params)
                conditions['pre_execution_table_exists_check'] = (
                    substitute_params(conditions['pre_execution_table_exists_check'],
                                      sql_params))
                sql_list[sql_file] = sql
            # use same conditions value for all

            LOGGER.info(sql_list)
            # alter the view to hide the new partition before it is ready
            if 'document_details' in table_name:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/create_document_details_stage_1_view.sql')], conditions, output_location)
            else:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/create_stage_1_view.sql')], conditions, output_location)

            # create a consolidated partition
            if 'document_details' in table_name:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/create_document_details_partition.sql')], conditions, output_location)
            else:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/create_partition.sql')], conditions, output_location)

            # attach the consolidated partition to the consolidated table
            if 'document_details' in table_name:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/add_document_details_partition.sql')], conditions, output_location)
            else:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/add_partition.sql')], conditions, output_location)

            # alter the view to show the new partition instead of the granualar partitions
            if 'document_details' in table_name:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/create_document_details_stage_2_view.sql')], conditions, output_location)
            else:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/create_stage_2_view.sql')], conditions, output_location)

            # remove the partitions from the recent table
            # remove partitions 25 at a time
            path_name_list_sub_list = list(splitlist(path_name_list, 25))
            for path_name_list_sub in path_name_list_sub_list:
                if path_name_list_sub:
                    sql_alter = 'ALTER TABLE {0} DROP IF EXISTS '.format(table_name)
                    sql_partitions = ','.join(path_name_list_sub)
                    sql = sql_alter + sql_partitions
                    LOGGER.info('About to execute sql:')
                    LOGGER.info(sql)
                    execute_athena(sql, conditions, output_location)

            # switch the view back to having no conditions in
            if 'document_details' in table_name:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/create_document_details_standard_view.sql')], conditions, output_location)
            else:
                execute_athena(sql_list[os.path.join(transform_dir, 'sql/create_standard_view.sql')], conditions, output_location)

        else:
            LOGGER.info('No partitions found')

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def splitlist(l, n):
    """
    Split lists to deal with maximums in Athena calls
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

def check_query_status(execution_id):
    """
    Loop until the query is either successful or fails

    Args:
        execution_id             : the submitted query execution id

    Returns:
        None
    """
    try:
        client = boto3.client('athena', config=CONFIG)
        LOGGER.info('About to check Athena status on SQL')
        while True:
            response = client.get_query_execution(
                QueryExecutionId=execution_id)
            if response['QueryExecution']['Status']['State'] in ('FAILED', 'SUCCEEDED', 'CANCELLED'):
                return response
            LOGGER.info('Sleeping for 1 second')
            time.sleep(1)

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

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

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        response = bucket.objects.filter(Prefix=path_to_delete).delete()
        LOGGER.info(response)

        if not response:
            LOGGER.info('Nothing to delete')
        else:
            LOGGER.info('The following was deleted: %s', response[0]['Deleted'])

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def execute_athena(sql, conditions, output_location):
    """
    Run SQL on Athena.

    Args:
        sql             : the SQL to execute
        conditions      : dict of optional pre and post execution conditions
        output_location : the S3 location for Athena to put the results

    Returns:
        None
    """

    try:
        if conditions['pre_execution_pause_seconds'] > 0:
            LOGGER.info('Pre execution pause for %s seconds.',
                        conditions['pre_execution_pause_seconds'])
            time.sleep(conditions['pre_execution_pause_seconds'])
        if conditions['pre_execution_table_exists_check'] != 'None':
            LOGGER.info('Checking for existence of table  %s',
                        conditions['pre_execution_table_exists_check'])
            table_exists_check(conditions['pre_execution_table_exists_check'])

        LOGGER.info('About to execute SQL:')
        sql_log = {}
        sql_log['sql'] = sql
        LOGGER.info(sql_log)
        client = boto3.client('athena', config=CONFIG)

        attempts = 8
        i = 1
        while True:
            if i == attempts:
                LOGGER.error('%s attempts made. Failing with error', attempts)
                sys.exit(1)
            try:
                response = client.start_query_execution(
                    QueryString=sql,
                    QueryExecutionContext={
                        'Database': GLUE_DATABASE
                    },
                    ResultConfiguration={
                        'OutputLocation': output_location
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
                LOGGER.info('Athena query submitted. Continuing.')
                LOGGER.info(response)
                response = check_query_status(response['QueryExecutionId'])
                if response['QueryExecution']['Status']['State'] == 'CANCELLED':
                    LOGGER.warning(response)
                    LOGGER.info('SQL query cancelled. Waiting %s second(s) before trying again', 2 ** i)
                    time.sleep((2 ** i) + random.random())
                    i += 1
                    clear_down(sql)
                if response['QueryExecution']['Status']['State'] == 'FAILED':
                    LOGGER.warning(response)
                    state_change_reason = response['QueryExecution']['Status']['StateChangeReason']
                    compiled = re.compile("Table*does not exist")
                    if "Query exhausted resources at this scale factor" in state_change_reason \
                       or "Partition metadata not available" in state_change_reason \
                       or "INTERNAL_ERROR" in state_change_reason \
                       or "ABANDONED_QUERY" in state_change_reason \
                       or "HIVE_PATH_ALREADY_EXISTS" in state_change_reason \
                       or "HIVE_CANNOT_OPEN_SPLIT" in state_change_reason \
                       or compiled.match(state_change_reason):
                        LOGGER.info('SQL query failed. Waiting %s second(s) before trying again', 2 ** i)
                        time.sleep((2 ** i) + random.random())
                        i += 1
                        clear_down(sql)
                    else:
                        LOGGER.error('SQL query failed and this type of error will not be retried. Exiting with failure.')
                        sys.exit(1)
                elif response['QueryExecution']['Status']['State'] == 'SUCCEEDED':
                    LOGGER.info('SQL statement completed successfully with the following statistics:')
                    LOGGER.info(response['QueryExecution']['Statistics'])
                    if response['QueryExecution']['Statistics']['DataScannedInBytes'] < conditions['min_scan_bytes']:
                        LOGGER.error('DataScannedInBytes is below expected minimum %s.',
                                     conditions['min_scan_bytes'])
                        LOGGER.error('Exiting with failure')
                        sys.exit(1)
                    break


    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def substitute_params(sql, sql_params):
    """
    Substitute SQL dict of parameter values

    Args:
        sql              : sql statement
        sql_params       : dict of parameters to substitute

    Returns:
        string containing SQL with parameters substituted in
    """

    for param_name in sql_params:
        sql = sql.replace(('{' + '{0}'.format(param_name) + '}'),
                          sql_params[param_name])
    return sql


def extract_conditions(sql):
    """
    Extract conditions from the the start of the SQL file

    Args:
       sql               : sql statement including conditions specified at start of file


    Returns:
       sql               : sql statement without conditions specified at start of file
       conditions        : dict of pre and post execution conditions
    """

    conditions = {'min_scan_bytes': 0,
                  'pre_execution_pause_seconds': 0,
                  'pre_execution_table_exists_check': 'None'}
    sql_output = []
    for line in sql.split('\n'):
        if line.startswith('#min_scan_bytes'):
            conditions['min_scan_bytes'] = int(line.split(':')[1])
            LOGGER.info('Setting min_scan_bytes: %s',
                        conditions['min_scan_bytes'])
        elif line.startswith('#pre_execution_pause_seconds'):
            conditions['pre_execution_pause_seconds'] = int(line.split(':')[1])
            LOGGER.info('Setting pre_execution_pause_seconds: %s',
                        conditions['pre_execution_pause_seconds'])
        elif line.startswith('#pre_execution_table_exists_check'):
            conditions['pre_execution_table_exists_check'] = line.split(':')[1]
            LOGGER.info('Setting pre_execution_table_exists_check: %s',
                        conditions['pre_execution_table_exists_check'])
        else:
            sql_output.append(line)
    LOGGER.info('Conditions: %s', conditions)
    return ('\n'.join(sql_output), conditions)


def read_sql_file(sql_filename, sql_params):
    """
    Read SQL from file and substitute parameters.

    Args:
        sql_filename     : the filename
        sql_params       : dict of parameters to substitute

    Returns:
        tuple string containing SQL with parameters substituted in
        followed by dict of conditions for SQL execution
    """

    try:
        file = open(sql_filename, "r")
        LOGGER.info('Opened the sql file %s', sql_filename)
        sql = file.read()
        (sql, conditions) = extract_conditions(sql)
        sql = substitute_params(sql, sql_params)
        LOGGER.info('Replaced parameters.')
        return (sql, conditions)
    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def get_path_name(key_name):
    """
    Get path name from key name

    Args:
        key_name

    Returns:
        path_name
    """

    keysplit = key_name.split('/')
    return '/'.join(keysplit[0:len(keysplit)-1])


def get_file_name(key_name):
    """
    Get file name from key name

    Args:
        key_name

    Returns:
        file_name
    """

    return key_name.split('/')[-1]

# pylint: disable=unused-argument
def lambda_handler(event, context):
    """
    Respond to triggering event by running Athena SQL.

    Args:
        event (dict)           : Data about the triggering event
        context (LamdaContext) : Runtime information

    Returns:
        null
    """

    try:
        global LOG_GROUP_NAME
        global LOG_STREAM_NAME
        LOG_GROUP_NAME = context.log_group_name
        LOG_STREAM_NAME = context.log_stream_name

        LOGGER.info('Last updated in framework version: %s', VERSION)
        LOGGER.info('Output Bucket: %s', OUTPUT_BUCKET_NAME)
        LOGGER.info('Glue Database: %s', GLUE_DATABASE)
        LOGGER.info('Namespace: %s', NAMESPACE)

        LOGGER.info('Event: %s', event)

        if event['Records'][0].get('s3'):
            LOGGER.info('Removing log/ prefix if event is triggered from the log')
            event['Records'][0]['s3']['object']['key'] = event['Records'][0]['s3']['object']['key'].replace('log/', '')
            LOGGER.info('Event: %s', event)
            input_bucket_name = event['Records'][0]['s3']['bucket']['name']
            key_name = urllib.parse.unquote_plus(
                event['Records'][0]['s3']['object']['key'])
            path_name = get_path_name(key_name)
            file_name = get_file_name(key_name)

            # Standard parameter section - RLS
            if event['Records'][0].get('pathNameRlsMax'):
                path_name_rls_max = event['Records'][0].get('pathNameRlsMax')
            else:
                path_name_rls_max = '2099-12-31'
            if event['Records'][0].get('pathNameRlsAgeDays'):
                path_name_rls_age_days = int(event['Records'][0].get('pathNameRlsAgeDays'))
            else:
                path_name_rls_age_days = 30
            path_name_rls_min = (datetime.datetime.utcnow()-datetime.timedelta(days=path_name_rls_age_days)).strftime("%Y-%m-%d")
            if event['Records'][0].get('pathNameRlsMin'):
                path_name_rls_min = event['Records'][0].get('pathNameRlsMin')
            # Standard parameter section - OAG
            if event['Records'][0].get('pathNameOagMax'):
                path_name_oag_max = event['Records'][0].get('pathNameOagMax')
            else:
                path_name_oag_max = '2099-12-31'
            if event['Records'][0].get('pathNameOagAgeDays'):
                path_name_oag_age_days = int(event['Records'][0].get('pathNameOagAgeDays'))
            else:
                path_name_oag_age_days = 30
            path_name_oag_min = (datetime.datetime.utcnow()-datetime.timedelta(days=path_name_oag_age_days)).strftime("%Y-%m-%d")
            if event['Records'][0].get('pathNameOagMin'):
                path_name_oag_min = event['Records'][0].get('pathNameOagMin')
            # Standard parameter section - ACL
            if event['Records'][0].get('pathNameAclMax'):
                path_name_acl_max = event['Records'][0].get('pathNameAclMax')
            else:
                path_name_acl_max = '2099-12-31'
            if event['Records'][0].get('pathNameAclAgeDays'):
                path_name_acl_age_days = int(event['Records'][0].get('pathNameAclAgeDays'))
            else:
                path_name_acl_age_days = 30
            path_name_acl_min = (datetime.datetime.utcnow()-datetime.timedelta(days=path_name_acl_age_days)).strftime("%Y-%m-%d")
            if event['Records'][0].get('pathNameAclMin'):
                path_name_acl_min = event['Records'][0].get('pathNameAclMin')
            # Standard parameter section - CS
            rnm_path_name_cs_max = '20991231'
            if event['Records'][0].get('pathNameCsMax'):
                path_name_cs_max = event['Records'][0].get('pathNameCsMax')
            else:
                path_name_cs_max = '2099-12-31'
            if event['Records'][0].get('pathNameCsAgeDays'):
                path_name_cs_age_days = int(event['Records'][0].get('pathNameCsAgeDays'))
            else:
                path_name_cs_age_days = 15
            path_name_cs_min = (datetime.datetime.utcnow()-datetime.timedelta(days=path_name_cs_age_days)).strftime("%Y-%m-%d")
            rnm_path_name_cs_min = (datetime.datetime.utcnow()-datetime.timedelta(days=path_name_cs_age_days)).strftime("%Y%m%d")
            if event['Records'][0].get('pathNameCsMin'):
                path_name_cs_min = event['Records'][0].get('pathNameCsMin')

        else:
            input_bucket_name = 'default'
            key_name = 'default'
            path_name = 'default'
            file_name = 'default'
            path_name_rls_min = 'default'
            path_name_rls_max = 'default'
            path_name_oag_min = 'default'
            path_name_oag_max = 'default'
            path_name_acl_min = 'default'
            path_name_acl_max = 'default'
            path_name_cs_min = 'default'
            path_name_cs_max = 'default'
            rnm_path_name_cs_min = 'default'
            rnm_path_name_cs_max = 'default'

        instance = get_instance()
        time_now = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        instance = instance + '_{0}'.format(time_now)

        LOGGER.info('Bucket name: %s', input_bucket_name)
        LOGGER.info('Path name: %s', path_name)
        LOGGER.info('File name: %s', file_name)
        LOGGER.info('Key name: %s', key_name)

        if not file_name:
            LOGGER.error('No file found in S3. Exiting with error')
            sys.exit(1)

        if path_name != 'default' and prefix_exists(
                        OUTPUT_BUCKET_NAME[5:],
                        'log-api-cross-record-scored/' + path_name):
            return

        if event['Records'][0].get('transformDir'):
            transform_dir = event['Records'][0].get('transformDir')
        else:
            transform_dir = get_transform_dir(file_name)
        LOGGER.info('Transform dir: %s', transform_dir)

        # set defaults which could be overridden
        min_path_name = 'default'
        max_path_name = 'default'
        consolidated_path_name = 'default'

        consolidation_target = event['Records'][0].get('consolidationTarget')
        if consolidation_target:
            LOGGER.info('Consolidation Target: %s', consolidation_target)
            if 'minPathName' in event:
                min_path_name = event['Records'][0].get('minPathName')
            # assume CW scheduled daily trigger at 1am
            elif event['Records'][0].get('schedule_type') == 'daily':
                min_path_name = '1900-01-01/00:00:00'
            # assume CW scheduled trigger at 10 past each hour
            elif event['Records'][0].get('schedule_type') == 'hourly':
                min_path_name = '1900-01-01/00:00:00'
            LOGGER.info('Min Path Name: %s', min_path_name)
            if 'maxPathName' in event:
                max_path_name = event['Records'][0].get('maxPathName')
            elif event['Records'][0].get('schedule_type') == 'daily':
                dt = datetime.date.today() + datetime.timedelta(days=1)
                max_path_name = datetime.datetime.combine(dt, datetime.datetime.min.time())
                max_path_name = max_path_name.strftime('%Y-%m-%d/%H:%M:%S')
            elif event['Records'][0].get('schedule_type') == 'hourly':
                now = datetime.datetime.utcnow() + datetime.timedelta(hours=0)
                max_path_name = now.strftime("%Y-%m-%d/%H:00:00")
            LOGGER.info('Max Path Name: %s', max_path_name)
            if 'consolidatedPathName' in event:
                consolidated_path_name = event['Records'][0].get('consolidatedPathName')
            elif event['Records'][0].get('schedule_type') == 'daily':
                dt = datetime.date.today()
                consolidated_path_name = datetime.datetime.combine(dt, datetime.datetime.min.time())
                consolidated_path_name = consolidated_path_name.strftime('%Y-%m-%d') + '-history'
            elif event['Records'][0].get('schedule_type') == 'hourly':
                consolidated_path_name = datetime.datetime.utcnow().strftime("%Y-%m-%d/%H:%M:%S.%f-consolidated")

            LOGGER.info('Consolidated path name: %s', consolidated_path_name)


        default_output = '{0}/working/default-output/'.format(
            OUTPUT_BUCKET_NAME)

        log_output = '{0}/log/{1}/'.format(
            OUTPUT_BUCKET_NAME, path_name)


        sql_params = {'input-bucket-name': 's3://{0}'.format(input_bucket_name),
                      'bucket-name': OUTPUT_BUCKET_NAME,
                      'path-name': path_name,
                      'file-name': file_name,
                      'instance': instance,
                      'namespace': NAMESPACE,
                      'path-name-rls-min': path_name_rls_min,
                      'path-name-rls-max': path_name_rls_max,
                      'path-name-oag-min': path_name_oag_min,
                      'path-name-oag-max': path_name_oag_max,
                      'path-name-acl-min': path_name_acl_min,
                      'path-name-acl-max': path_name_acl_max,
                      'path-name-cs-min': path_name_cs_min,
                      'path-name-cs-max': path_name_cs_max,
                      'rnm-path-name-cs-min': rnm_path_name_cs_min,
                      'rnm-path-name-cs-max': rnm_path_name_cs_max,
                      'consolidated-path-name': consolidated_path_name}

        print(sql_params)
        if consolidation_target:
            drop_partitions_athena(consolidation_target,
                                   min_path_name,
                                   max_path_name,
                                   default_output,
                                   transform_dir,
                                   sql_params)

            if (event['Records'][0].get('schedule_type') == 'hourly') and ('document_details' not in consolidation_target):

                # write additional triggers
                with open("/tmp/trigger.csv", "w") as f:
                    f.write("API consolidation complete.")

                target_bucket_name = OUTPUT_BUCKET_NAME[5:]

                upload_s3_object(
                    '/tmp/trigger.csv',
                    target_bucket_name,
                    'log-consolidator/' + consolidated_path_name + '/trigger.csv')

                LOGGER.info('Trigger upload complete')

        else:
            for sql_file in get_sql_files(transform_dir):
                (sql, conditions) = read_sql_file(sql_file,
                                                  sql_params)
                conditions['pre_execution_table_exists_check'] = (
                    substitute_params(conditions['pre_execution_table_exists_check'],
                                      sql_params))
                if '/log' in sql_file:
                    sql_output = log_output
                else:
                    sql_output = default_output
                    execute_athena(sql,
                                   conditions,
                                   sql_output)

            # write additional triggers
            with open("/tmp/trigger.csv", "w") as f:
                f.write("API processing complete.")

            target_bucket_name = OUTPUT_BUCKET_NAME[5:]

            upload_s3_object(
                '/tmp/trigger.csv',
                target_bucket_name,
                'log-api-cross-record-scored/' + path_name + '/trigger.csv')

            LOGGER.info('Trigger upload complete')

        LOGGER.info("We're done here.")
        return event

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)
