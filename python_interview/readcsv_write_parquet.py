import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa

df = pd.read_csv('/Users/sbommireddy/Downloads/bx_test_data.csv')
print("---------------")
print(type(df))
print("---------------")

table = pa.Table.from_pandas(df, preserve_index=False)
#write parquet file with SNAPPY Compression.
#In PyArrow we use Snappy compression by default
pq.write_table(table, 'bx_test_data.snappy.parquet', compression='snappy')
pq.write_table(table, 'bx_test_data.gzip.parquet', compression='gzip')
