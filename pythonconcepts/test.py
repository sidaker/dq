import csv
import os

cdate= "2020-04-08"

print(type(cdate))
print(cdate)

#read from csv  and assign to ddate

high_water_mark=''
with open(os.path.join('/tmp','highwatermark.csv')) as f:
    reader = csv.reader(f)
    high_water_mark = next(reader)  # gets the first line
    cdate = high_water_mark[0]
    #LOGGER.info('High Water Mark: %s', high_water_mark)
    print(high_water_mark)
    print(cdate)

with open("/tmp/highwatermark.csv", "w") as f:
    f.write(cdate)


#write to csv
#read from csv  and assign to edate
with open(os.path.join('/tmp','highwatermark.csv')) as f:
    reader = csv.reader(f)
    high_water_mark = next(reader)  # gets the first line
    #LOGGER.info('High Water Mark: %s', high_water_mark)
    print(high_water_mark)

# /Users/sbommireddy/opt/anaconda3/bin/python /Users/sbommireddy/Documents/python/assignments/dq/boto3/invoke_lambda_async_prod1.py
