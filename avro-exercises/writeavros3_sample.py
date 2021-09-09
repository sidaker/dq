from writeavro import writeavrofiles3

avsch_file = '/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises/schemas/city.avsc'
avdata_file='/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises//data/city.avro'
avwriterobj = writeavrofiles3.AvroS3Writer(avsch_file,avdata_file)
avwriterobj.write_sample()
avwriterobj.upload_to_aws(avdata_file,'s3-dq-test-prac-1','test/mywoohootest.avro')
