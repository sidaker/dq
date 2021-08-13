import pyarrow.parquet as pq
import s3fs

s3 = s3fs.S3FileSystem()

pandas_dataframe = pq.ParquetDataset('s3://s3-dq-cdlz-btid-input/btid/DataFeedId=5/2020-01-27/bx_test_data.snappy.parquet', filesystem=s3).read_pandas().to_pandas()

print(pandas_dataframe)
