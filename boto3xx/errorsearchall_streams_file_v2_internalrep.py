"""Print log event messages from a CloudWatch log group.

Usage: errorsearchall_streams_file_v2.py <LOG_GROUP_NAME> [--start=<START>] [--end=<END>] [--stream_prefix=<STREAM_PREFIX>]
       errorsearchall_streams_file_v2.py -h --help

python errorsearchall_streams_file_v2_internalrep.py " \
/aws/lambda/internal-reporting-prod-lambda-athena"

/Users/sbommireddy/Documents/python/assignments/dq/boto3xx/errorsearchall_streams_file_v2_internalrep.py

python errorsearchall_streams_file_v2_internalrep.py \
"/aws/lambda/internal-reporting-prod-lambda-athena" \
--start= \
--end= \
--stream_prefix="2022/02/01/"

       sed -n -e 's/^.*FAILED//p' analyse_fail > analyse_fail4

Known Issue:
 at 'logStreamNames' failed to satisfy constraint: Member must have length less than or equal to 100

Options:
  <LOG_GROUP_NAME>    Name of the CloudWatch log group.
  --start=<START>     Only print events with a timestamp after this time
                      (expressed as milliseconds after midnight Jan 1, 1970).
  --end=<END>         Only print events with a timestamp before this time
                      (expressed as milliseconds after midnight Jan 1, 1970).
  --stream_prefix=<STREAM_PREFIX>   Only print events with a timestamp before this time
  -h --help           Show this screen.

"""


import docopt
import boto3
import csv
import os
import datetime
import re
import ast

# python errorsearch_streams.py "/aws/lambda/api-record-level-score-notprod-lambda-athena"
# Always keep the doc string to the start of the file (before the import line)
# python errorsearch_streams_file.py /aws/lambda/api-kafka-input-test-lambda

def list_log_groups(env):
    """
    Lists the specified log groups.
    You can list all your log groups or filter the results by prefix.
    """
    session = boto3.Session(profile_name=env)
    client = session.client('logs',region_name='eu-west-2')
    limit=50

    kwargs = {
        'logGroupNamePrefix': log_group,
        'limit': limit,

    }

    while True:
        resp = client.describe_log_groups(**kwargs)
        yield from resp['logGroups']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break


def list_log_streams(env,log_group,limit,prefix=None):
    """
    Lists log streams with a log group.
    You can list all your log groups or filter the results by prefix.
    """
    session = boto3.Session(profile_name=env)
    client = session.client('logs',region_name='eu-west-2')
    if(prefix is None):
        kwargs = {
            'logGroupName': log_group,
            'limit': limit,
            'descending': True,
            'orderBy': 'LastEventTime',
        }

        while True:
            resp = client.describe_log_streams(**kwargs)
            yield from resp['logStreams']
            try:
                kwargs['nextToken'] = resp['nextToken']
            except KeyError:
                break

    else:
        # response = client.describe_log_streams(
        # logGroupName=log_group,
        # logStreamNamePrefix=prefix,
        # limit=limit)
        kwargs = {
            'logGroupName': log_group,
            'limit': limit,
            'logStreamNamePrefix': prefix,
        }

        while True:
            resp = client.describe_log_streams(**kwargs)
            yield from resp['logStreams']
            try:
                kwargs['nextToken'] = resp['nextToken']
            except KeyError:
                break

    #return response['logStreams']
    #return response


def get_error_log_events(env,log_group,stream_list,limit=50):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    session = boto3.Session(profile_name=env)
    client = session.client('logs',region_name='eu-west-2')
    kwargs = {
        'logGroupName': log_group,
        'logStreamNames': stream_list,
        'filterPattern': "already exists",
        'limit': limit,
                }

    while True:
        # BUG: works only for the first filter pattern.
        # Works fine when used with out **kwargs.
        resp = client.filter_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break

    #return resp['events']


def get_log_events(env,log_group,limit=50):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    session = boto3.Session(profile_name=env)
    client = session.client('logs',region_name='eu-west-2')
    kwargs = {
        'logGroupName': log_group,
        'limit': limit,
        }

    while True:
        resp = client.filter_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break


def get_log_events_timerange(env,log_group,limit,st,et):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    session = boto3.Session(profile_name=env)
    client = session.client('logs',region_name='eu-west-2')
    #resp = client.filter_log_events(logGroupName=log_group, limit=limit, startTime=st,endTime=et)
    #return resp['events']
    kwargs = {
        'logGroupName': log_group,
        'limit': limit,
        'startTime': st,
        'endTime':et ,
        }
    while True:
        resp = client.filter_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break


def get_events_by_stream(env,log_group,logStreamName,limit=50):
    '''
    '''
    session = boto3.Session(profile_name=env)
    client = session.client('logs',region_name='eu-west-2')
    # response = client.get_log_events(
    #     logGroupName=logGroupName,
    #     logStreamName=logStreamName,
    #     limit=limit,
    #     startFromHead=True
    #     )
    # return response['events']
    kwargs = {
        'logGroupName': log_group,
        'logStreamName': logStreamName,
        'limit': limit,
        'startFromHead': True,
        }
    while True:
        resp = client.get_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break


if __name__ == '__main__':
    #env='notprod'
    env='prod'
    #env='default'
    # export AWS_DEFAULT_REGION=us-west-2
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    session = boto3.Session(profile_name=env)
    local_output_dir='/Users/sbommireddy/Downloads/cloudwatchlogs/'

    args = docopt.docopt(__doc__)
    log_group = args['<LOG_GROUP_NAME>']

    filename = 'logs_'  + str(datetime.datetime.now()) + '.csv'
    logfile = os.path.join(local_output_dir, env, filename)
    print(logfile)

    if args['--start']:
        start_time = int(args['--start'])
    else:
        start_time = None
    if args['--end']:
        end_time = int(args['--end'])
    else:
        end_time = None

    if args['--stream_prefix']:
        stream_prefix = args['--stream_prefix']
    else:
        stream_prefix = None


    client = session.client('logs')
    print("List Recent Log Events")
    limit=50


    if not os.path.exists(os.path.join(local_output_dir, env)):
        os.makedirs(os.path.join(local_output_dir, env))
    liststream=[]

    if(stream_prefix is None):
        print("List Recent Log Streams of", log_group)
        for lstream in list_log_streams(env,log_group,limit):
            #print(lstream['logStreamName'])
            liststream.append(lstream['logStreamName'])
    else:
        print("List Log Streams by Prefix:",stream_prefix)
        for lstream in list_log_streams(env,log_group,limit,stream_prefix):
            #print(lstream['logStreamName'])
            liststream.append(lstream['logStreamName'])

    print("Searching for errors..Listing Log Streams")

    with open(logfile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["LogStreamName", "timestamp","MessageType","Timestamp","Status", "fullmessage","StatusMessage"])
        # liststream ensure lenth is < 100.
        print(len(liststream))
        chunks = [liststream[x:x+99] for x in range(0, len(liststream), 99)]
        print(len(chunks))

        for lstream in chunks:
            for event in get_error_log_events(env,log_group,lstream,limit):
                print("Stream:",event['logStreamName'])
                print("UnixTimestamp:",event['timestamp'])
                print("MessageType:",event['message'].split("	")[0])
                try:
                    tsp = event['message'].split("	")[1]
                except IndexError:
                    tsp = 'null'

                try:
                    stats = event['message'].split("	")[3]
                except IndexError:
                    stats = 'null'

                try:
                    if stats.startswith('{') :
                        rstats1 = re.search(r'\b(Status)\b', stats)
                        index= rstats1.start()
                        rstats = stats[index:]

                    else:
                        rstats = ''


                except Exception as inst:
                    #print("Error Parsing")
                    print(inst)
                    rstats = 'CP'


                print('**************************')
                writer.writerow([event['logStreamName'], event['timestamp'], event['message'].split("	")[0],tsp, stats, event['message'], rstats])
