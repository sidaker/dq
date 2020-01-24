# pylint: disable=broad-except
"""
Copy files from one S3 location to another
"""
import json
import logging
import urllib.parse
import urllib.request
import sys
import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import time

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOG_GROUP_NAME = None
LOG_STREAM_NAME = None

CONFIG = Config(
    retries=dict(
        max_attempts=20
    )
)

def error_handler(lineno, error, fail=True):

    try:
        LOGGER.error('The following error has occurred on line: %s', lineno)
        LOGGER.error(str(error))
        sess = boto3.session.Session()
        region = sess.region_name

        message = "https://{0}.console.aws.amazon.com/cloudwatch/home?region={0}#logEventViewer:group={1};stream={2}".format(region, LOG_GROUP_NAME, LOG_STREAM_NAME)

        send_message_to_slack('Pipeline error: {0}'.format(message))
        if fail:
            sys.exit(1)

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)
        LOGGER.error(
            'The following error has occurred on line: %s',
            sys.exc_info()[2].tb_lineno)
        LOGGER.error(str(err))
        sys.exit(1)

def send_message_to_slack(text):
    """
    Formats the text provides and posts to a specific Slack web app's URL

    Args:
        text : the message to be displayed on the Slack channel

    Returns:
        Slack API repsonse
    """

    try:
        post = {"text": "{0}".format(text)}

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


def parse_message(message_text):
    """
    Parse the content of the SNS message

    Args:
        message_text (string) : The message supplied by SNS

    Returns:
        {status, dataFeedTaskId, dataFeedId}
    """
    try:
        message_split = message_text.split('\n')
        if 'COMPLETED' not in message_split[3]:
            LOGGER.info('This is not a successful completion message.')
            return {'status': False}
        if 'dataFeedTaskId' not in message_split[1] or 'dataFeedId' not in message_split[2]:
            LOGGER.info('This is not a valid completion message.')
            return {'status': False}
        dataFeedTaskId = int(message_split[1].split(' ')[1])
        dataFeedId = int(message_split[2].split(' ')[1])
        return {'status': True, 'dataFeedTaskId': dataFeedTaskId, 'dataFeedId': dataFeedId}

    except Exception as err:
        LOGGER.error(
            'The following error has occurred on line: %s',
            sys.exc_info()[2].tb_lineno)
        LOGGER.error(str(err))


def copy_s3_files(input_bucket_name, output_bucket_name, input_path, output_path):
    """
    Copies files

    Args:
        input_bucket_name : The name of the source bucket (without the s3:// prefix)
        output_bucket_name : The name of the target bucket (without the s3:// prefix)
        input_path: The source path
        output_path: The target path

    Returns:
        None
    """
    try:
        s3_conn = boto3.resource('s3', config=CONFIG)
        input_bucket = s3_conn.Bucket(input_bucket_name)
        output_bucket = s3_conn.Bucket(output_bucket_name)
        LOGGER.info('The following objects were found:')
        for input_bucket_object in input_bucket.objects.filter(Prefix=input_path):
            if input_bucket_object.key != input_path:
                LOGGER.info(input_bucket_object)
                filename = input_bucket_object.key.split('/')[-1]
                ts = time.time()
                timestamp_date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timestamp_time = datetime.fromtimestamp(ts).strftime('%H:%M:%S.%f')
                if 'PARSED' in input_bucket_object.key.upper():
                    output_path = output_path_parsed
                    required_file = True
                elif 'RAW' in input_bucket_object.key.upper():
                    output_path = output_path_raw
                    required_file = True
                else:
                    LOGGER.info('This is not a PARSED or RAW file, not copying.')
                    required_file = False
                if required_file:
                    output_bucket_object = output_bucket.Object(output_path +
                                           timestamp_date + '/' +
                                           timestamp_time + '/' +
                                           filename)
                    copy_source = {'Bucket': input_bucket_object.bucket_name,
                                   'Key': input_bucket_object.key}
                    output_bucket_object.copy(copy_source)
                    LOGGER.info('Copied {0} to {1}'.format(input_bucket_object, output_bucket_object))
                    time.sleep(0.1)
        return

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


# pylint: disable=unused-argument
def lambda_handler(event, context):
    """
    Respond to an SNS notification.

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

        LOGGER.info('The following event was received:')
        LOGGER.info(event)

        circuit_breaker_parameter_name = os.environ['circuit_breaker_parameter_name']
        input_bucket_name = os.environ['input_bucket_name']
        LOGGER.info('input_bucket_name:{0}'.format(input_bucket_name))
        output_bucket_name = os.environ['output_bucket_name']
        LOGGER.info('output_bucket_name:{0}'.format(output_bucket_name))
        input_path = os.environ['input_path']
        LOGGER.info('input_path:{0}'.format(input_path))
        output_path_parsed = os.environ['output_path_parsed']
        LOGGER.info('output_path_parsed:{0}'.format(output_path_parsed))
        output_path_raw = os.environ['output_path_raw']
        LOGGER.info('output_path_raw:{0}'.format(output_path_raw))

        ssm = boto3.client('ssm', config=CONFIG)
        response = ssm.get_parameters(
            Names=[
                circuit_breaker_parameter_name])
        for param in response['Parameters']:
            if param['Name'] == circuit_breaker_parameter_name:
                circuit_breaker_parameter_value = param['Value']

        LOGGER.info('Got SSM parameters. Continuing.')

        if circuit_breaker_parameter_value != 'y':
            LOGGER.info('This lambda is not enabled. No further processing will occur')
        else:
            client = boto3.client('stepfunctions', config=CONFIG)
            account_id = boto3.client('sts').get_caller_identity().get('Account')
            LOGGER.info('This lambda is enabled.')

        parsed_message = parse_message(event['Records'][0]['Sns']['Message'])
        LOGGER.info('The parsed message appears as follows:')
        LOGGER.info(parsed_message)

        today = datetime.today().strftime('%Y-%m-%d')
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        for day in [today, yesterday]:
            input_path_constructed = (input_path +
                                      'CollectionDate=' +
                                      day +
                                      '/DataFeedId=' +
                                      str(parsed_message['dataFeedId']) +
                                      '/DataFeedTaskId=' +
                                      str(parsed_message['dataFeedTaskId']) +
                                      '/')
            LOGGER.info('input_path_constructed:{0}'.format(input_path_constructed))
            copy_s3_files(input_bucket_name,
                          output_bucket_name,
                          input_path_constructed,
                          output_path)

        LOGGER.info("We're done here")

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)
