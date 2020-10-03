import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa
from collections import OrderedDict, defaultdict

#Read a single parquet file locally like this:

path = '/Users/sbommireddy/Downloads/part-00000-a73df3f7-caee-4241-a654-53549099e97d-c000.snappy.parquet'
table = pq.read_table(path)
df = table.to_pandas()

# recordid=1024764
# recordid=1024597 Remove. Filter the two.
# documenttype=P,nationality,documenttype

print(df['body'].head())
print(df.info())
#print(df['body']['recordid'].head())
print(df.count())
# 1771049

dfh = df['body']
print(dfh.head())
print(type(dfh))
print(dfh.count())

'''
df1 = dfh.loc[df['RecordID']!='1024764', :]
df2 = df1.loc[df1['RecordID']!='1024597', :]

print(df2.count())
'''

#print(dfh.head())

dict1 = dfh.to_dict(into=OrderedDict)

for x,y in dict1.items():
    print(x)
    print(y)
    print(y['RecordID'])
    if(y['RecordID']=='1024764' or y['RecordID']=='1024597'):
        del dict1[x]
        print("Removed element")
        print(y['RecordID'])

# Convert Ordered dict back to pandas series.
