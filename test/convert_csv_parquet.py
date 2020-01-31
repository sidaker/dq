import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa

df = pd.read_csv('/Users/sbommireddy/Documents/python/assignments/dq/test/bitd_3000k.csv')

table = pa.Table.from_pandas(df, preserve_index=False)
#write parquet file
pq.write_table(table, '/Users/sbommireddy/Documents/python/assignments/dq/test/bitd_3000k.snappy.parquet', compression='snappy')

parquet_file1 = pq.ParquetFile('/Users/sbommireddy/Documents/python/assignments/dq/test/bitd_3000k.snappy.parquet')
print("Print metadata")
print(parquet_file1.metadata)
print(parquet_file1.schema)
