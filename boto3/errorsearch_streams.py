"""Print log event messages from a CloudWatch log group.

Usage: errorsearch_streams.py <LOG_GROUP_NAME> [--start=<START>] [--end=<END>]
       errorsearch_streams.py -h --help

Options:
  <LOG_GROUP_NAME>    Name of the CloudWatch log group.
  --start=<START>     Only print events with a timestamp after this time
                      (expressed as milliseconds after midnight Jan 1, 1970).
  --end=<END>         Only print events with a timestamp before this time
                      (expressed as milliseconds after midnight Jan 1, 1970).
  -h --help           Show this screen.

"""


import docopt
import boto3
import csv
import os

# python errorsearch_streams.py "/aws/lambda/api-record-level-score-notprod-lambda-athena"
# Always keep the doc string to the start of the file (before the import line)

def list_log_groups():
    """
    Lists the specified log groups.
    You can list all your log groups or filter the results by prefix.
    """
    session = boto3.Session(profile_name='notprod')
    client = session.client('logs',region_name='eu-west-2')
    response = client.describe_log_groups(
    logGroupNamePrefix='/aws/lambda/',
    limit=10)

    return response['logGroups']


def list_log_streams(log_group,limit,prefix=None):
    """
    Lists log streams with a log group.
    You can list all your log groups or filter the results by prefix.
    """
    session = boto3.Session(profile_name='notprod')
    client = session.client('logs',region_name='eu-west-2')
    if(prefix is None):
        response = client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LastEventTime',
        descending=True,
        limit=limit)
    else:
        response = client.describe_log_streams(
        logGroupName=log_group,
        logStreamNamePrefix=prefix,
        limit=limit)


    return response['logStreams']
    #return response


def get_error_log_events(log_group,stream_list,limit):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    session = boto3.Session(profile_name='notprod')
    client = session.client('logs',region_name='eu-west-2')
    resp = client.filter_log_events(
    logGroupName=log_group,
    logStreamNames=stream_list,
    #filterPattern='WARNING ? ERROR',
    # [w1=ERROR || w1=WARN, w2]
    filterPattern='ERROR ? WARNING',
    limit=limit)

    return resp['events']


def get_log_events(log_group,limit):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    session = boto3.Session(profile_name='notprod')
    client = session.client('logs',region_name='eu-west-2')
    resp = client.filter_log_events(logGroupName=log_group, limit=limit)
    return resp['events']


def get_log_events_timerange(log_group,limit,st,et):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    session = boto3.Session(profile_name='notprod')
    client = session.client('logs',region_name='eu-west-2')
    resp = client.filter_log_events(logGroupName=log_group, limit=limit, startTime=st,endTime=et)
    return resp['events']


def get_events_by_stream(logGroupName,logStreamName,limit):
    '''
    '''
    session = boto3.Session(profile_name='notprod')
    client = session.client('logs',region_name='eu-west-2')
    response = client.get_log_events(
        logGroupName=logGroupName,
        logStreamName=logStreamName,
        limit=limit,
        startFromHead=True
        )
    return response['events']

if __name__ == '__main__':
    env='notprod'
    session = boto3.Session(profile_name=env)
    stream_prefix=None
    local_output_dir='/Users/sbommireddy/Downloads/cloudwatchlogs/'
    filename = "mylogs.csv"
    logfile = os.path.join(local_output_dir, env, filename)
    args = docopt.docopt(__doc__)
    log_group = args['<LOG_GROUP_NAME>']
    if args['--start']:
        start_time = int(args['--start'])
    else:
        start_time = None
    if args['--end']:
        end_time = int(args['--end'])
    else:
        end_time = None


    client = session.client('logs')
    print("List Recent Log Events")
    #log_group = '/aws/lambda/api-kafka-input-test-lambda'
    #log_group = '/aws/lambda/api-record-level-score-test-lambda-athena'
    #log_group='/aws/lambda/api-accuracy-scoring-test-lambda-athena'
    #log_group='/aws/lambda/api-record-level-score-test-lambda-athena'
    #log_group='/aws/lambda/api-record-level-score-test-lambda-athena'
    #Stream: 2020/07/10/[$LATEST]b264200b1ff54133b60d07c898d67fec

    #log_group='/aws/lambda/api-record-level-score-notprod-lambda-athena'
    limit=50
    stream_prefix='2020/07/11'

    if not os.path.exists(os.path.join(local_output_dir, env)):
        os.makedirs(os.path.join(local_output_dir, env))


    liststream=[]

    if(stream_prefix is None):
        print("List Recent Log Streams")
        for lstream in list_log_streams(log_group,limit):
            #print(lstream['logStreamName'])
            liststream.append(lstream['logStreamName'])
    else:
        print("List Log Streams by Prefix:",stream_prefix)
        for lstream in list_log_streams(log_group,limit,stream_prefix):
            #print(lstream['logStreamName'])
            liststream.append(lstream['logStreamName'])

    print("Searching for errors")
    #print(liststream)
    #get_error_log_events(log_group,liststream,limit)
    #get_log_events_timerange(log_group,limit,start_time,end_time)

    with open(logfile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["LogStreamName", "timestamp", "fullmessage"])
        for event in get_error_log_events(log_group,liststream,limit):
            #print(event)
            print("Stream:",event['logStreamName'])
            print("Timestamp:",event['timestamp'])
            print("Message:",event['message'])
            print('**************************')

            writer.writerow([event['logStreamName'], event['timestamp'], event['message']])


        #Write all Streams, Timestamps and Messages to a file.
        #Parse each message and extract for Athena failures, Query Execution id, Status and StateChangeReason
