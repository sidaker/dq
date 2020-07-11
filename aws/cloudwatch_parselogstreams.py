import boto3


# /aws/lambda/api-cross-record-scored-test-lambda-athena
# /aws/lambda/api-record-level-score-test-lambda-athena
# /aws/lambda/api-kafka-input-test-lambda


def get_log_events(log_group,limit):
    """List the first 10 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    client = boto3.client('logs',region_name='eu-west-2')
    resp = client.filter_log_events(logGroupName=log_group, limit=limit)
    return resp['events']


if __name__ == '__main__':
    print("List Recent Log Streams")
    log_group = '/aws/lambda/api-kafka-input-test-lambda'
    #log_group = '/aws/lambda/api-record-level-score-test-lambda-athena'

    limit=10
    for event in get_log_events(log_group,limit):
        print(event)
