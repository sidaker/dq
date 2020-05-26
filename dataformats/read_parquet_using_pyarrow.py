import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa

#Read a single parquet file locally like this:

path = "/Users/sbommireddy/Documents/python/assignments/dq/dataformats/part-00000-4e165a94-46c6-43bb-919e-706543c5dd8f-c000.snappy.parquet"
table = pq.read_table(path)
df = table.to_pandas()
print(df)
print(table.schema)

#Read a directory of parquet files locally like this:
#dataset = pq.ParquetDataset('parquet/')
#table = dataset.read()
#df = table.to_pandas()
