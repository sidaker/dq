import pyarrow.parquet as pq
import numpy as np
import pandas as pd
import pyarrow as pa

df = pd.read_csv('/Users/sbommireddy/Downloads/bx_test_data.csv')
table = pa.Table.from_pandas(df, preserve_index=False)
#write parquet file
pq.write_table(table, 'bx_test_data_noindex.parquet')

#write parquet file with SNAPPY Compression.
# In PyArrow we use Snappy compression by default
pq.write_table(table, 'bx_test_data.snappy.parquet', compression='snappy')

pq.write_table(table, 'bx_test_data.gzip.parquet', compression='gzip')

pq.write_table(table, 'bx_test_data.none.parquet', compression='none')

#Read parquet.
t = pq.read_table('bx_test_data_noindex.parquet')

print(t.to_pandas())

parquet_file1 = pq.ParquetFile('bx_test_data_noindex.parquet')
print("Print metadata")
print(parquet_file1.metadata)
print(parquet_file1.schema)


parquet_file2 = pq.ParquetFile('bx_test_data.snappy.parquet')
print("Print metadata of SNAPPY compressed")
print(parquet_file2.metadata)

parquet_file3 = pq.ParquetFile('bx_test_data.gzip.parquet')
print("Print metadata of gzip compressed")
print(parquet_file3.metadata)

parquet_file4 = pq.ParquetFile('bx_test_data.none.parquet')
print("Print metadata of no compressed")
print(parquet_file4.metadata)
