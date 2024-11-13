# pylint: disable=broad-except
"""
Triggers the api and gait downstream pipelines
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
    Respond to an S3 event notification.

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

        input_bucket_name = event['Records'][0]['s3']['bucket']['name']
        key_name = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key'])
        path_name = get_path_name(key_name)
        file_name = get_file_name(key_name)

        LOGGER.info('Bucket name: %s', input_bucket_name)
        LOGGER.info('Path name: %s', path_name)
        LOGGER.info('Key name: %s', key_name)

        if not file_name:
            LOGGER.warning('No file found in S3. This may be an empty path creation. Exiting with warning')
            return

        circuit_breaker_parameter_name = os.environ['circuit_breaker_parameter_name']
        LOGGER.info('circuit_breaker_parameter_name: %s',
                    circuit_breaker_parameter_name)
        state_machine_name = os.environ['state_machine_name']
        LOGGER.info('state_machine_name: %s',
                    state_machine_name)

        gait_circuit_breaker_parameter_name = os.environ['gait_circuit_breaker_parameter_name']
        LOGGER.info('gait_circuit_breaker_parameter_name: %s',
                    gait_circuit_breaker_parameter_name)
        gait_state_machine_name = os.environ['gait_state_machine_name']
        LOGGER.info('gait_state_machine_name: %s',
                    gait_state_machine_name)

        raw_file_index_circuit_breaker_parameter_name = os.environ['raw_file_index_circuit_breaker_parameter_name']
        LOGGER.info('raw_file_index_circuit_breaker_parameter_name: %s',
                    raw_file_index_circuit_breaker_parameter_name)
        raw_file_index_state_machine_name = os.environ['raw_file_index_state_machine_name']
        LOGGER.info('raw_file_index_state_machine_name: %s',
                    raw_file_index_state_machine_name)

        ssm = boto3.client('ssm', config=CONFIG)
        response = ssm.get_parameters(
            Names=[
                circuit_breaker_parameter_name,
                gait_circuit_breaker_parameter_name,
                raw_file_index_circuit_breaker_parameter_name])
        for param in response['Parameters']:
            if param['Name'] == circuit_breaker_parameter_name:
                circuit_breaker_parameter_value = param['Value']
            if param['Name'] == gait_circuit_breaker_parameter_name:
                gait_circuit_breaker_parameter_value = param['Value']
            if param['Name'] == raw_file_index_circuit_breaker_parameter_name:
                raw_file_index_circuit_breaker_parameter_value = param['Value']

        LOGGER.info('Got SSM parameters. Continuing.')

        if circuit_breaker_parameter_value != 'y':
            LOGGER.info('API lambda is not enabled. No further processing will occur')
        else:
            client = boto3.client('stepfunctions', config=CONFIG)
            account_id = boto3.client('sts').get_caller_identity().get('Account')
            LOGGER.info('About to start the following state machine: %s', state_machine_name)

            response = client.start_execution(
                stateMachineArn=(
                    'arn:aws:states:eu-west-2:{0}:stateMachine:{1}'.format(
                        account_id,
                        state_machine_name)),
                input=json.dumps(event))
            LOGGER.info('The start_execution AWS api provided the following response:')
            LOGGER.info(response)

        if gait_circuit_breaker_parameter_value != 'y':
            LOGGER.info('GAIT lambda is not enabled. No further processing will occur')
        else:
            client = boto3.client('stepfunctions', config=CONFIG)
            account_id = boto3.client('sts').get_caller_identity().get('Account')
            LOGGER.info('About to start the following state machine: %s', gait_state_machine_name)

            response = client.start_execution(
                stateMachineArn=(
                    'arn:aws:states:eu-west-2:{0}:stateMachine:{1}'.format(
                        account_id,
                        gait_state_machine_name)),
                input=json.dumps(event))
            LOGGER.info('The start_execution AWS api provided the following response:')
            LOGGER.info(response)

        if raw_file_index_circuit_breaker_parameter_value != 'y':
            LOGGER.info('RAW lambda is not enabled. No further processing will occur')
        else:
            client = boto3.client('stepfunctions', config=CONFIG)
            account_id = boto3.client('sts').get_caller_identity().get('Account')
            LOGGER.info('About to start the following state machine: %s', raw_file_index_state_machine_name)

            response = client.start_execution(
                stateMachineArn=(
                    'arn:aws:states:eu-west-2:{0}:stateMachine:{1}'.format(
                        account_id,
                        raw_file_index_state_machine_name)),
                input=json.dumps(event))
            LOGGER.info('The start_execution AWS api provided the following response:')
            LOGGER.info(response)

        LOGGER.info("We're done here")

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)
