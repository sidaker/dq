import boto3



def list_log_groups():
    """
    Lists the specified log groups.
    You can list all your log groups or filter the results by prefix.
    """
    client = boto3.client('logs',region_name='eu-west-2')
    response = client.describe_log_groups(
    logGroupNamePrefix='/aws/lambda/',
    limit=10)

    return response['logGroups']


def list_log_streams(log_group,limit):
    """
    Lists log streams with a log group.
    You can list all your log groups or filter the results by prefix.
    """
    client = boto3.client('logs',region_name='eu-west-2')
    response = client.describe_log_streams(
    logGroupName=log_group,
    orderBy='LastEventTime',
    descending=True,
    limit=limit)

    return response['logStreams']
    #return response


def get_error_log_events(log_group,stream_list,limit):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    client = boto3.client('logs',region_name='eu-west-2')
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
    client = boto3.client('logs',region_name='eu-west-2')
    resp = client.filter_log_events(logGroupName=log_group, limit=limit)
    return resp['events']


def get_log_events_timerange(log_group,limit,st,et):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    client = boto3.client('logs',region_name='eu-west-2')
    resp = client.filter_log_events(logGroupName=log_group, limit=limit, startTime=st,endTime=et)
    return resp['events']


def get_events_by_stream(logGroupName,logStreamName,limit):
    '''
    '''
    client = boto3.client('logs',region_name='eu-west-2')
    response = client.get_log_events(
        logGroupName=logGroupName,
        logStreamName=logStreamName,
        limit=limit,
        startFromHead=True
        )
    return response['events']

if __name__ == '__main__':
    print("List Recent Log Events")
    #log_group = '/aws/lambda/api-kafka-input-test-lambda'
    #log_group = '/aws/lambda/api-record-level-score-test-lambda-athena'
    #log_group='/aws/lambda/api-accuracy-scoring-test-lambda-athena'
    #log_group='/aws/lambda/api-record-level-score-test-lambda-athena'
    log_group='/aws/lambda/api-record-level-score-test-lambda-athena'


    limit=30
    liststream=[]
    print("List Recent Log Streams")
    for lstream in list_log_streams(log_group,limit):
        #print(lstream['logStreamName'])
        liststream.append(lstream['logStreamName'])

    print("Searching for errors")
    #print(liststream)
    #get_error_log_events(log_group,liststream,limit)

    for event in get_error_log_events(log_group,['2020/07/09/[$LATEST]0856210b7cd4468fa24757eda7b827b2'],limit):
        print(event)

    for event in get_error_log_events(log_group,liststream,limit):
        print(event)
