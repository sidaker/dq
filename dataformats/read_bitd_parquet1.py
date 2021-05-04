import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa
from collections import OrderedDict, defaultdict

#Read a single parquet file locally like this:
# Change nested value.

path = '/Users/sbommireddy/Downloads/part-00000-8f415f02-1301-4021-90bf-0aaae2b75b84-c000.snappy.parquet'
parquet_file = pq.ParquetFile(path)
print(parquet_file.metadata)
print(parquet_file.schema)
print(parquet_file.num_row_groups)
print("*"*50)
table = pq.read_table(path)
df = table.to_pandas()

print(df['body'].head())
print(df.info())
print("***___"*50)
print(df.count())
# 1771049

dfh = df['body']
print(dfh.head())
print(type(dfh))
print(dfh.count())



dict1 = dfh.to_dict(into=OrderedDict)

print("$"*50)
for x,y in dict1.items():
    print(x)
    print(y)
    print(y['RecordId'])
    # 2020-12-02 17:11:33
    print(y['DateAcquired'])

# Convert Ordered dict back to pandas series.
# pq.write_table(table, 'bx_test_data.snappy.parquet', compression='snappy')
myschema = parquet_file.schema

# writer = pq.ParquetWriter('/Users/sbommireddy/Downloads/parquest_user_defined_schema.parquet', schema=myschema)
# TypeError: Argument 'schema' has incorrect type (expected pyarrow.lib.Schema, got pyarrow._parquet.ParquetSchema)
# writer.write_table(table)
