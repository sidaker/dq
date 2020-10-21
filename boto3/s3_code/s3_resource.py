import boto3
s3_resource = boto3.resource('s3')

#Create a new bucket
#s3_resource.create_bucket(Bucket="first-aws-bucket-1")

for bucket in s3_resource.buckets.all():
    print(bucket.name)

# Upload an object to S3
# s3_resource.Object('first-aws-bucket-1', 'Screen_Shot.png').\
#     upload_file(Filename='/Users/ankhipaul/Documents/Screenshots/Screen_Shot.png')

# Download an object from S3
# s3_resource.Object('pythonusecase', 'doc.pdf').download_file(
#     f'/Users/ankhipaul/Documents/doc.pdf')


# List all objects of a bucket

print("*"*50)

pythonusecase = s3_resource.Bucket(name = 's3-dq-cdl-s3-s4-test')
for object in pythonusecase.objects.all():
          print(object.key)


#Copy an object to a new location within the same bucket with a new name
#s3_resource.Object("s3-dq-cdl-s3-s4-test", "new_convertcsv.csv").copy_from(CopySource="pythonusecase/old_convertcsv.csv")


# Delete an object
#s3_resource.Object("pythonusecase", "old_convertcsv.csv").delete()


# Delete a bucket. First delete all objects.
# bucket = s3_resource.Bucket('first-aws-bucket-1')
# bucket.objects.all().delete()
# s3_resource.Bucket("first-aws-bucket-1").delete()
