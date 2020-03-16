import pyarrow.parquet as pq
import pandas as pd
import pyarrow as pa

df = pd.read_csv('/Users/sbommireddy/Downloads/bx_test_data.csv')

# What is Pyarrow Table?
# classpyarrow.Table is a Pyarrow class.
# What is table variable type here?

table = pa.Table.from_pandas(df, preserve_index=False)
#write parquet file with SNAPPY Compression.
#In PyArrow we use Snappy compression by default
pq.write_table(table, 'bx_test_data.snappy.parquet', compression='snappy')
pq.write_table(table, 'bx_test_data.gzip.parquet', compression='gzip')
