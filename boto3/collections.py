import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# make sure AWS_REGION is set and exported to the environment
# export AWS_DEFAULT_REGION="us-west-2"
'''
A collection provides an iterable interface to a group of resources.
Collections behave similarly to Django QuerySets and expose a similar API.
A collection seamlessly handles pagination for you, making it possible to easily iterate over all items from all pages of data.
'''

session = boto3.Session(profile_name='notprod')
sqsclient = session.client('sqs',region_name='eu-west-2')
s3client = session.client('s3',region_name='eu-west-2')


s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')

# SQS list all queues
try:
    for queue in sqs.queues.all():
        print(queue.url)
except Exception as err:
    print(err)

for bucket in s3.buckets.all():
    print(bucket.name)


buckets = list(s3.buckets.all())

#It is possible to limit the number of items returned from a collection by using either the limit() method:

print("List first 2 buckets")
# S3 iterate over first 2 buckets
for bucket in s3.buckets.limit(2):
    print(bucket.name)

# Filtering
'''
Behind the scenes, the below example will call ListBuckets, ListObjects, and HeadObject many times.
 If you have a large number of S3 objects then this could incur a significant cost.
'''
print("Testing filtering")
for bucket in s3.buckets.all():
    for obj in bucket.objects.filter(Prefix='btid/'):
        print('{0}:{1}'.format(bucket.name, obj.key))


'''
Collection methods are chainable.
They return copies of the collection rather than modifying the collection, including a deep copy of any associated operation parameters.
'''
