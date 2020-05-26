import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa

#Read a single parquet file locally like this:

path = 'parquet/part-r-00000-1e638be4-e31f-498a-a359-47d017a0059c.gz.parquet'
table = pq.read_table(path)
df = table.to_pandas()

#Read a directory of parquet files locally like this:
dataset = pq.ParquetDataset('parquet/')
table = dataset.read()
df = table.to_pandas()
