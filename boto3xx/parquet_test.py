import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa

df = pd.read_csv('/Users/sbommireddy/Downloads/parquest_3.csv')
table = pa.Table.from_pandas(df, preserve_index=False)
#write parquet file with SNAPPY Compression.
# In PyArrow we use Snappy compression by default
pq.write_table(table, 'parquest_3.snappy.parquet', compression='snappy')
