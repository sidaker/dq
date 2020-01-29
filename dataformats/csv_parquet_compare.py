import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa

df = pd.read_csv('/Users/sbommireddy/Downloads/business-price-indexes-september-2019-quarter-csv.csv')
table = pa.Table.from_pandas(df, preserve_index=False)
#write parquet file
pq.write_table(table, 'business-price-indexes-september-2019-quarter.parquet')


t = pq.read_table('business-price-indexes-september-2019-quarter.parquet')

print(t.to_pandas())

parquet_file1 = pq.ParquetFile('business-price-indexes-september-2019-quarter.parquet')
print("Print metadata")
print(parquet_file1.metadata)
